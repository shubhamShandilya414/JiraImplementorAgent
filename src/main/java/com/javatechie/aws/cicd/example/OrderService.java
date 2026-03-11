package com.javatechie.aws/cicd/example;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class OrderService {

    @Autowired
    private OrderDao orderDao;

    public List<Order> getOrders(Double minPrice, int page, int size) {
        // NEW: Added filtering and pagination
        List<Order> orders = orderDao.getOrders();
        if (minPrice != null) {
            orders = orders.stream().filter(order -> order.getPrice() >= minPrice).collect(Collectors.toList());
        }
        int start = page * size;
        int end = start + size;
        return orders.subList(start, Math.min(end, orders.size()));
    }

    public Order getOrderById(int id) {
        // NEW: Added order retrieval by ID
        return orderDao.getOrders().stream().filter(order -> order.getId() == id).findFirst().orElse(null);
    }
}