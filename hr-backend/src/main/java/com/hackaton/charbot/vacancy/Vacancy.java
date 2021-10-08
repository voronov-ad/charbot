package com.hackaton.charbot.vacancy;

import lombok.Data;

import java.util.List;

@Data
public class Vacancy {
    String id;
    String title;
    String companyName;
    String description;
    String employeeMode;
    String experience;
    String link;
    String salary;
    List<String> tags;
    Company company;
}
