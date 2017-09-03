# PythonTools
描述：<br/>
这个项目只是一个带IoC、模板引擎、ORM的MVC框架！！<br/>
只是写了一个用于加密，hash，和根据模板生成带动态参数的url工具页面。<br/>

用到的主要三方框架：<br/>
模板引擎用了Iinja2，<br/>
数据库驱动用了pymssql，<br/>
http服务用了aiohttp，<br/>
协程用了asyncio，<br/>

目的：<br/>
最终我希望把它改造成一个Wechat接口程序+后台程序。<br/>

其他：<br/>
我的第一个python项目，基本参考了廖雪峰大牛的文档（<a href="https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000">python教程</a>）,他的文档很有条理，料也很足，很适合初学者进行一个全面的摸底。<br/>
我挺佩服他，个人觉得一个能将一个复杂的知识领域有取舍、有条理的写出高可读性的Doc，需要很大的知识量、熟练度，和对技术执着。<br/>
当然他的文档只是入门和启迪的作用，最重要的还是得从官方文档和技术社区寻找更专一的，优雅的实现。<br/>

项目说明：<br/>
这个项目框架我用了很久，可扩展性很强，复杂度很低。较适合中等大小的项目开发。<br/>
依赖关系：<br/>
  Common：不依赖任何其他模块；<br/>
  Entity：不依赖任何其他模块；<br/>
  Model：不依赖与任何其他模块；<br/>
  Services：依赖于Common；<br/>
  Decorator：依赖于Common；<br/>
  Repository：依赖于Entity，和Common；<br/>
  Buiness：依赖于Repository，Entity，Model，Common；<br/>
  MVC：依赖于其他的所有模块；<br/>
  
这个项目从目录上来看->
  Common模块：通用的工具类，<br/>
  Entity模块：作为数据库对象容器，<br/>
  Model模块：作为View的数据源，有时Entity的字段和类型并不适合直接返回给View使用，<br/>
  Services模块：用于与外部接口打交道，依赖于Common，有自己的Model与外界进行通讯，<br/>
  Decorator模块：对我来说这一层应该分配到View层更合适，但是因为不同于Asp.Net程序的过滤器，Decorato可以用于所有的class和function，所以我抽出来作为单独的一层使用，<br/>
   Repository模块：直接与数据库打交道，<br/>
   Buiness模块：用于处理业务，Model与Entity之间的转换等作用，<br/>
   MVC模块：最终输出的一层，没有逻辑，至于简单的数据操作。<br/>
 
 
description:<br/>
This project is just an MVC framework with IoC, template engine, ORM! The
Just write a url tool page for encryption, hash, and generate dynamic parameters with templates based on the template.<br/>

The main tripartite framework used:<br/>
The template engine uses Iinja2,<br/>
Database driven with pymssql,<br/>
http service with aiohttp,<br/>
The association uses asyncio,<br/>

purpose:<br/>
Eventually I would like to transform it into a Wechat interface program + daemon.<br/>

other:<br/>
My first python project, the basic reference Liao Xuefeng Daniel's documentation (<a href="https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000">python tutorial</a>), his documentation is very organized, the material is also very full, it is suitable for beginners to conduct a comprehensive thoroughly.<br/>
I admire him personally, I feel that a complex knowledge of the field can choose, organized to write a high degree of readability Doc, requires a lot of knowledge, proficiency, and technical dedication.<br/>
Of course, his document is only the role of entry and inspiration, the most important thing is to get from the official documents and technical community more specific, elegant realization.<br/>

project instruction:<br/>
This project framework I used for a long time, highly scalable, very low complexity. More suitable for medium-sized project development.<br/>
Dependencies:
Common: does not depend on any other modules;<br/>
Entity: does not depend on any other module;<br/>
Model: does not depend on any other module;<br/>
Services: Depends on Common;<br/>
Decorator: depends on Common;<br/>
Repository: Depends on Entity, and Common;<br/>
Buiness: Depends on Repository, Entity, Model, Common;<br/>
MVC: Depends on all other modules;<br/>

This item from the directory point of view -> <br/>
Common module: a common tool class,<br/>
Entity module: as a database object container,<br/>
Model module: As a view of the data source, sometimes Entity field and type is not suitable for direct return to View use,<br/>
Services module: used to deal with the external interface, depending on the Common, have their own model to communicate with the outside world,<br/>
Decorator module: for me this layer should be assigned to the View layer is more appropriate, but because the filter is different from the Asp.Net program, Decorato can be used for all the class and function, so I extracted as a separate layer to use ,<br/>
Repository module: deal directly with the database,<br/>
Buiness module: used to deal with business, Model and Entity conversion between the role,<br/>
MVC module: the final output of a layer, no logic, as for the simple data operation.<br/>
  
