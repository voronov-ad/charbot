package com.hackaton.charbot.resume;

import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class ResumeSearcherClientImpl implements ResumeSearcherClient {

    public ResumeSearcherClientImpl(RestTemplateBuilder restTemplateBuilder) {
        this.restTemplate = restTemplateBuilder.build();
    }

    private final RestTemplate restTemplate;

    @Override
    public List<Resume> findRelatedResumes(String title) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        Map<String, Object> map = new HashMap<>();
        map.put("title", title);
        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(map, headers);
        Resume[] resumes = restTemplate.postForObject("http://resume-searcher:5000/resume-search", entity, Resume[].class);
        List<Resume> resumeList = List.of(resumes);
        resumeList.forEach(resume -> {
            String link = resume.getLink();
            int questionPosition = link.indexOf('?');
            resume.setId(link.substring(link.lastIndexOf('/') + 1, questionPosition));
            resume.setLink(link.substring(0, questionPosition));
        });
        return resumeList;
    }
}
