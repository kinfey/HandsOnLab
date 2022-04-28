package com.javademo.githubdemo;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("api")
public class APIController {

    //create weather api   
    @GetMapping("/weather/{city}")
    public String getWeather(@PathVariable String city) {
        return "Weather in " + city + " is good";
    }

    //return 1 to 50 even number
    @RequestMapping(value = "/even", method = RequestMethod.GET)
    public String getEven() {
        StringBuilder sb = new StringBuilder();
        for (int i = 1; i <= 50; i++) {
            if (i % 2 == 0) {
                sb.append(i).append(",");
            }
        }
        return sb.toString();
    }





    
}
