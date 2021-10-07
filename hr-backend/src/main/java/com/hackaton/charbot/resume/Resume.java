package com.hackaton.charbot.resume;

import lombok.Data;

import java.util.List;

@Data
public class Resume {
    String id;
    String link;
    String address;
    String age;
    String date_of_birth;
    String exprerience;
    Boolean has_education;
    List<String> languages;
    String last_work;
    String metro;
    String name;
    String position;
    String salary;
    List<String> skills;
    List<String> specialization;
    String specialization_category;
    String work_place_count;
}
