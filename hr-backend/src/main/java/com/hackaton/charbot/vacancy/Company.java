package com.hackaton.charbot.vacancy;

import lombok.Data;

import java.util.List;

@Data
public class Company {
    String name;
    Integer vacancies;
    List<String> area;
    String city;
    String description;
    String linkt;
}
