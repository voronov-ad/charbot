package com.hackaton.charbot;

import com.hackaton.charbot.resume.Resume;
import com.hackaton.charbot.resume.ResumeSearcherClient;
import com.hackaton.charbot.resume.ResumeStorage;
import com.hackaton.charbot.vacancy.Vacancy;
import com.hackaton.charbot.vacancy.VacancySearcherClient;
import com.hackaton.charbot.vacancy.VacancyStorage;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping(path = "/api/related-vacancy")
@RequiredArgsConstructor
public class RelatedVacancyController {

    private final VacancySearcherClient vacancyClient;
    private final ResumeSearcherClient resumeClient;
    private final VacancyStorage vacancyStorage;
    private final ResumeStorage resumeStorage;


    @GetMapping
    List<String> findRelated(@RequestParam("id") String id) {
        Vacancy vacancy = vacancyClient.findById(id);
        vacancyStorage.save(vacancy);
        String title = vacancy.getTitle();
        List<Resume> relatedResumes = resumeClient.findRelatedResumes(title);
        resumeStorage.save(relatedResumes);
        return relatedResumes.stream().map(Resume::getLink).collect(Collectors.toList());
    }
}
