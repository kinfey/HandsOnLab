package com.javahol.springcloudapp;


import com.azure.spring.data.cosmos.repository.ReactiveCosmosRepository;

public interface InfoRepository extends ReactiveCosmosRepository<Info,String> {
    
}
