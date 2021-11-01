package com.javahol.dockerjaveholdemo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class DockerjaveholdemoApplication {

	public static void main(String[] args) {
		SpringApplication.run(DockerjaveholdemoApplication.class, args);
	}

	
    @GetMapping("/info")
    public String info() {
        return "Spring Boot MicroService on Azure";
    }

}
