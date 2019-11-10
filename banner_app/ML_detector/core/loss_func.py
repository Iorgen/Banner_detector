from keras import backend as K
import tensorflow as tf
from keras.losses import binary_crossentropy


# TODO document all the loss type functions
# the actual loss calc occurs here despite it not being
# an internal Keras loss function
def ctc_lambda_func(args):
    """

    :param args:
    :return:
    """
    y_pred, labels, input_length, label_length = args
    # the 2 is critical here since the first couple outputs of the RNN
    # tend to be garbage:
    y_pred = y_pred[:, 2:, :]
    return K.ctc_batch_cost(labels, y_pred, input_length, label_length)


# Detection loss calculation Function
def detection_loss(grid_size):
    """

    :param grid_size:
    :return:
    """
    def get_box_highest_percentage(arr):
        shape = tf.shape(arr)

        reshaped = tf.reshape(arr, (shape[0], tf.reduce_prod(shape[1:-1]), -1))

        # returns array containing the index of the highest percentage of each batch
        # where 0 <= index <= height * width
        max_prob_ind = tf.argmax(reshaped[..., -1], axis=-1, output_type=tf.int32)

        # turn indices (batch, y * x) into (batch, y, x)
        # returns (3, batch) tensor
        unraveled = tf.unravel_index(max_prob_ind, shape[:-1])

        # turn tensor into (batch, 3) and keep only (y, x)
        unraveled = tf.transpose(unraveled)[:, 1:]
        y, x = unraveled[..., 0], unraveled[..., 1]

        # stack indices and create (batch, 5) tensor which
        # contains height, width, offset_y, offset_x, percentage
        indices = tf.stack([tf.range(shape[0]), y, x], axis=-1)
        box = tf.gather_nd(arr, indices)

        y, x = tf.cast(y, tf.float32), tf.cast(x, tf.float32)

        # transform box to (y + offset_y, x + offset_x, 6 * height, 6 * width, obj)
        # output is (batch, 5)
        out = tf.stack([y + box[..., 2], x + box[..., 3],
                        (grid_size - 1) * box[..., 0], (grid_size - 1) * box[..., 1],
                        box[..., -1]], axis=-1)

        return out

    def loss(y_true, y_pred):
        # get the box with the highest percentage in each image
        true_box = get_box_highest_percentage(y_true)
        pred_box = get_box_highest_percentage(y_pred)

        # object loss
        obj_loss = binary_crossentropy(y_true[..., 4:5], y_pred[..., 4:5])

        # mse with the boxes that have the highest percentage
        box_loss = tf.reduce_sum(tf.squared_difference(true_box[..., :-1], pred_box[..., :-1]))

        return tf.reduce_sum(obj_loss) + box_loss

    return loss
