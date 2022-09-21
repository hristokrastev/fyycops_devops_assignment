package com.example.demo;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class HelloWorldController {

    // private final RabbitTemplate rabbitTemplate;

    // @Autowired
    // public HomeController(RabbitTemplate rabbitTemplate) {
    //     this.rabbitTemplate = rabbitTemplate;
    // }

    // @GetMapping
    // public String rabbitHealth() {
    //     return "Health Checks!";
    // }

    @Value("${app.banner.label}")
    private String label;

    @Value("${app.banner.color}")
    private String color;

    @GetMapping("/")
	public String helloworld(
        @RequestParam(name="name", required=false, defaultValue="World")
        String name, Model model
    ) {
        model.addAttribute("label", label);
        model.addAttribute("color", color);
        model.addAttribute("name", name);
        return "helloworld";
	}

}
