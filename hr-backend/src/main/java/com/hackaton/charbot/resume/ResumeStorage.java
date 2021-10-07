package com.hackaton.charbot.resume;

import java.util.List;
import java.util.Optional;

public interface ResumeStorage {

    default void save(List<Resume> resumeList) {
        resumeList.forEach(this::save);
    }

    void save(Resume resume);

    Optional<Resume> findById(String id);

    List<Resume> findAll();
}
