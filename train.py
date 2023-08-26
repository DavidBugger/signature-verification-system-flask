import tensorflow as tf

# Load pre-trained MobileNetV2 model without top classification layer
base_model = tf.keras.applications.MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Create a new model with custom output layer for binary classification
output_layer = tf.keras.layers.Dense(1, activation='sigmoid')(base_model.layers[-1].output)
model = tf.keras.Model(inputs=base_model.inputs, outputs=output_layer)

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Save the entire model (architecture, weights, training configuration)
model.save('model/pretrained_signature_model_full.h5')

# Load the model
loaded_model = tf.keras.models.load_model('model/pretrained_signature_model_full.h5')

# Now the loaded model is fully configured for predictions
