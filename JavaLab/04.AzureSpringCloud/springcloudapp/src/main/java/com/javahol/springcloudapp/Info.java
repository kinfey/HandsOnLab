package com.javahol.springcloudapp;

import com.azure.spring.data.cosmos.core.mapping.Container;

import org.springframework.data.annotation.Id;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor

@Container(containerName = "Info")
public class Info {
    @Id
    public String id;
    public String location;
    
}
