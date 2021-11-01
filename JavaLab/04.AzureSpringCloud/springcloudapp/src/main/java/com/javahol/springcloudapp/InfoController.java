package com.javahol.springcloudapp;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;


import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;


@RestController
public class InfoController {

    
    private InfoRepository infoRepository;

    public InfoController(InfoRepository repository) {
        this.infoRepository = repository;
    }

    @PostMapping("/info")
    public ResponseEntity<String> updateInfo(@RequestBody Info info) {
        Mono<Info> saveUserMono = infoRepository.save(info);
        saveUserMono.block();
        return new ResponseEntity<>("Successfully insert", HttpStatus.OK);
    }

    @GetMapping("/info")
    public ResponseEntity<List<Info>> getAllInfo() {
       Flux<Info> infoList= infoRepository.findAll();
        return new ResponseEntity<>(infoList.collectList().block(), HttpStatus.OK);
    }
    
}
