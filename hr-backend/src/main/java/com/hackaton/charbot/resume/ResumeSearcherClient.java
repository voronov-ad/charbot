package com.hackaton.charbot.resume;

import java.util.List;

public interface ResumeSearcherClient {

    List<Resume> findRelatedResumes(String title);
}
