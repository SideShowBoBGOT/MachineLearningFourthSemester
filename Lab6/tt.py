model = {'epochs': 10,
    'layers': [{'units': 100, 'activation': 'sigmoid', 'input_shape': (3,)},
   {'units': 100, 'activation': 'sigmoid'},
   {'units': 2, 'activation': 'sigmoid'}]}
network = models.Sequential()
for l in model['layers']:
    network.add(layers.Dense(**l))
network.compile(optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy'])
network.fit(x_train, y_train, epochs=model['epochs'])
network.save(f'best_model.h5')