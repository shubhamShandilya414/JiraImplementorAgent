package com.javatechie.aws/cicd/example;

import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public class OrderDao {

    public List<Order> getOrders() {
        // Existing logic remains unchanged
        return java.util.Arrays.asList(
                new Order(101, "Mobile", 1, 300000),
                new Order(58, "Book", 4, 2000),
                new Order(205, "Laptop", 1, 150000),
                new Order(809, "headset", 1, 1799))
                .stream().sorted(Comparator.comparingInt(Order::getPrice)).collect(Collectors.toList());
    }
}