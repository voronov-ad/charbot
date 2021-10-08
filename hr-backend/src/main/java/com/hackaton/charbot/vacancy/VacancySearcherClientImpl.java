package com.hackaton.charbot.vacancy;

import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

@Service
public class VacancySearcherClientImpl implements VacancySearcherClient {


    public VacancySearcherClientImpl(RestTemplateBuilder restTemplateBuilder) {
        this.restTemplate = restTemplateBuilder.build();
    }

    private final RestTemplate restTemplate;

    @Override
    public Vacancy findById(String id) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        Map<String, Object> map = new HashMap<>();
        map.put("id", id);
        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(map, headers);
        Vacancy vacancy = restTemplate.postForObject("http://vacancy-searcher:5000/vacancy", entity, Vacancy.class);
        Company companyInfo = findCompanyInfo(vacancy.getCompanyName());
        vacancy.setId(id);
        vacancy.setCompany(companyInfo);
        return vacancy;
    }

    private Company findCompanyInfo(String companyName) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        Map<String, Object> map = new HashMap<>();
        map.put("name", companyName);
        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(map, headers);
        return restTemplate.postForObject("http://company-searcher:5000/company", entity, Company.class);
    }
}
