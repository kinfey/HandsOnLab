# **TensorFlow.NET** #

<img src="./image/03/03_001.png">

**TensorFlow 是一个端到端开源机器学习平台。它拥有一个全面而灵活的生态系统，其中包含各种工具、库和社区资源，可助力研究人员推动先进机器学习技术的发展，并使开发者能够轻松地构建和部署由机器学习提供支持的应用。**


<img src="./image/03/03_002.png">



## **感谢社区， .NET Core 除了原生的ML.NET ,也有社区的机器学习框架 TensorFlow** ##


<img src="./image/03/03_003.png">

https://github.com/SciSharp 

这里面有和TensorFlow同步的TensorFlow.NET ，让.NET 程序员无缝进入深度学习领域


<img src="./image/03/03_004.png">

https://github.com/SciSharp/TensorFlow.NET

**TensorFlow.NET (TF.NET) 为 TensorFlow 提供了 .NET Standard 绑定。 它旨在用 C# 实现完整的 Tensorflow API，允许 .NET 开发人员使用跨平台的 .NET Standard 框架开发、训练和部署机器学习模型。 TensorFlow.NET 内置了 Keras 高级接口，并作为独立包 TensorFlow.Keras 发布。**


```C#
#r "nuget: TensorFlow.Net"
#r "nuget: TensorFlow.Keras"
#r "nuget: SciSharp.TensorFlow.Redist"
#r "nuget: NumSharp"
```


```C#
using Tensorflow;
using static Tensorflow.Binding;
```


```C#
tf.enable_eager_execution();
```


```C#
var str = "Hello, TensorFlow.NET!";
var hello = tf.constant(str);
```


```C#
print(hello);
```


```C#
var tensor = hello.numpy();
```


```C#
tensor.ToString() 
```
