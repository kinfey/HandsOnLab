# **00.NOTE BOOK 环境安装** #

## **一.为何选择notebook ？** ##

Jupyter notebook（http://jupyter.org/） 是一种 Web 应用，能让用户将说明文本、数学方程、代码和可视化内容全部组合到一个易于共享的文档中。

**可选择语言:** 支持超过40种编程语言，包括Python、R、Julia、Scala等。

**分享笔记本:** 可以使用电子邮件、Dropbox、GitHub和Jupyter Notebook Viewer与他人共享。

**交互式输出:** 代码可以生成丰富的交互式输出，包括HTML、图像、视频、LaTeX等等。

**大数据整合:** 通过Python、R、Scala编程语言使用Apache Spark等大数据框架工具。支持使用pandas、scikit-learn、ggplot2、TensorFlow来探索同一份数据。


## **二.环境安装** ##

**1. Python环境安装**
       
jupyter notebook 基于Python， 机器必须有Python运行环境，建议安装3.8.x的环境

**Linux/macOS/WSL2 安装**

请参考docs文件夹下的00_Linux_WSL_MacOS_Install_Python.pdf

**Windows安装**

请参考docs文件夹下的00_Windows_Install_Python.pdf

**一些补充：**

Windows 下建议使用WSL2 来设置，关于WSL2 的文档(https://docs.microsoft.com/zh-cn/learn/modules/get-started-with-windows-subsystem-for-linux/ 搭配Ubuntu 20.04 来安装)

更具体的深度学习环境安装可以参考 https://blog.csdn.net/kinfey/article/details/117635067

**2. 安装Jupyter Notebook**

通过pip3 安装Jupyter 运行环境  

```zsh
pip3 install jupyter
```

运行jupyter

```zsh
jupyter notebook --no-browser
```

<img src='./image/00/00_002.png'>

**关于notebook 的更多使用 https://jupyter-notebook.readthedocs.io/en/stable/** 

**第一次运行notebook 会要求输入密码，这个时候你需要做的(https://jupyter-notebook.readthedocs.io/en/stable/public_server.html)**

**3. 关于.NETCore 版本**

建议使用5.0.x 版本 https://dotnet.microsoft.com/download




## **三.关于.NET Interactive** ##

官方的话 .NET Interactive takes the power of .NET and embeds it into your interactive experiences. Share code, explore data, write, and learn across your apps in ways you couldn't before. 就是一个更灵活的代码交互方式，专注于数据浏览与整理 **(注意：如果你没有安装好Python和Jupyter环境参参考本文档的第二点完成)**

**1. 通过dotnet tools 安装.NET Interactive**

```zsh
dotnet tool install --global Microsoft.dotnet-interactive
```
一些提示 dotnet tool 需要配置全局PATH ，否则会影响dotnet-interactive的运行
(关于 dotnet tool path 的文档可以参考 https://docs.microsoft.com/en-us/dotnet/core/tools/dotnet-tool-install)

**2. 把.NET Interactive 绑定到Jupyter Notebook**

```zsh
dotnet-interactive jupyter install
```

**3. 运行检查**

```zsh
jupyter kernelspec list
```

<img src='./image/00/00_004.png'>


## **四.Visual Studio Code 的.NET Interactive插件** ##

**1.安装Visual Studio Code (https://code.visualstudio.com/)**

**2.安装.NET Interactive 插件**


<img src='./image/00/00_001.png'>

## **五. 例子** ##

**1. 基本CSharp运行**


```C#
Console.WriteLine("Hello World , Reactor")
```


```C#
using System;
using System.Text.Json;
using System.Text.Json.Serialization;
```


```C#
public class ReactorInfo
{
    public string Name { get; set; }
    public string Title { get; set; }
}

```


```C#
var info = new ReactorInfo{ Name = "Kinfey", Title ="Reactor Guest" };
```


```C#
string infoString = JsonSerializer.Serialize(info);
```


```C#
Console.WriteLine(infoString);
```

**2. Nuget引入**

Blazor 引入到Notebook
(https://github.com/plbonneville/RazorInteractive)


```C#
#r "nuget: RazorInteractive, 1.0.5"
```


```C#
#!razor

@{
    var colors = new [] { "red", "green", "blue" };
}

<ol>
@foreach(var color in colors)
{
    <li style="color: @color;">@color</li>
}
</ol>
```


```C#
var firstname = "John";
var lastname = "Doe";
var colors = new [] { "red", "green", "blue" };
```


```C#
#!razor

<p>Hello <b>@Model.firstname @Model.lastname</b>, what is you favorite a color?</p>

<ol>
@foreach(var color in Model.colors)
{
    <li style="color: @color;">@color</li>
}
</ol>
```
