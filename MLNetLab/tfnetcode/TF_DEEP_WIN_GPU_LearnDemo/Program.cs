using System;
using System.Collections.Generic;
using Tensorflow;
using Tensorflow.Keras;
using static Tensorflow.Binding;
using static Tensorflow.KerasApi;
using Tensorflow.Keras.Utils;
using System.IO;
using System.Diagnostics;
using Tensorflow.Keras.Engine;

namespace TF_DEEP_WIN_GPU_LearnDemo
{

    class Program
    {
        static int batch_size = 50;
        static int epochs = 3;
        //static Shape img_dim = (180, 180);
        static IDatasetV2 train_ds, val_ds;
        static Model model;
        static void DownloadImage()
        {
            string data_dir = Directory.GetCurrentDirectory() + "/image/flower_photos";

            train_ds = keras.preprocessing.image_dataset_from_directory(data_dir,
                validation_split: 0.2f,
                subset: "training",
                seed: 123,
                image_size: (32, 32),
                batch_size: batch_size);

            val_ds = keras.preprocessing.image_dataset_from_directory(data_dir,
            validation_split: 0.2f,
            subset: "validation",
            seed: 123,
            image_size: (32, 32),
            batch_size: batch_size);

            train_ds = train_ds.shuffle(1000).prefetch(buffer_size: -1);
            val_ds = val_ds.prefetch(buffer_size: -1);


        }
        static void BuildModel()
        {
            int num_classes = 5;
            // var normalization_layer = tf.keras.layers.Rescaling(1.0f / 255);
            var layers = keras.layers;
            model = keras.Sequential(new List<ILayer>
            {
                layers.Rescaling(1.0f / 255, input_shape: (32, 32, 3)),
                layers.Conv2D(16, 3, padding: "same", activation: keras.activations.Relu),
                layers.MaxPooling2D(),
                layers.Flatten(),
                layers.Dense(128, activation: keras.activations.Relu),
                layers.Dense(num_classes)
            });

            model.compile(optimizer: keras.optimizers.Adam(),
                loss: keras.losses.SparseCategoricalCrossentropy(from_logits: true),
                metrics: new[] { "accuracy" });

            model.summary();
        }

        static void TrainModel()
        {
            

            model.fit(train_ds, validation_data: val_ds, epochs: epochs);
            string data_dir = Directory.GetCurrentDirectory() + "\\output\\";
            model.save(data_dir+"models.h5");
        }

        static void Main(string[] args)
        {
            tf.enable_eager_execution();

            
            // var gpus = tf.config.list_physical_devices("GPU");

            // tf.config.experimental.set_memory_growth(gpus[0], true);

            // Tensorflow.Device.PhysicalDevice device = new Tensorflow.Device.PhysicalDevice();

            // device.DeviceName = "GPU";
                        
            var sw = new Stopwatch();
            try
            {
                    sw.Restart();
                    DownloadImage();
                    BuildModel();
                    TrainModel();
                    sw.Stop();
            }
            catch (Exception ex)
            {
                //errors.Add($"Example: {example.Config.Name}");
                Console.WriteLine(ex);
            }

            
            keras.backend.clear_session();

        }
    }
}
