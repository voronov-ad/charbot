package com.hackaton.charbot.feedback;

import lombok.Data;

@Data
public class Feedback {
    String id;
    String url_vacancy;
    String url_candidate;
    Integer label;
}
