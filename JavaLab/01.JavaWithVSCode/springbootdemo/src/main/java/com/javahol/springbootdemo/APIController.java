package com.javahol.springbootdemo;

import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("api")
public class APIController {

    
    @RequestMapping(value = "/getInfo/{name}",method = RequestMethod.GET)
    public String getInfo(@PathVariable String name){
        return "Hi ," + name ;
    }


    
}