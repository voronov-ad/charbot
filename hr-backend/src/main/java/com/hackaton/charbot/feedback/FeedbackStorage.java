package com.hackaton.charbot.feedback;

import java.util.List;
import java.util.Optional;

public interface FeedbackStorage {

    Integer save(Feedback feedback);

    Optional<Feedback> findById(String id);

    List<Feedback> findAll();
}
