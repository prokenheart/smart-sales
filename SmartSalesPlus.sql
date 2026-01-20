insert into price (product_id, price_amount, price_date) VALUES
('03b4aa18-6462-4af1-b727-97364244893c', 999.99, '2025-01-15'),
('2a18d461-5f4c-4cc5-b041-224ce76fc240', 799.99, '2025-02-20'),
('ebb53f41-cf0f-4502-be3a-7776f515512a', 199.99, '2025-03-10'),
('4e14ea35-f250-4e8f-940b-0149d156699b', 299.99, '2025-04-05'),
('95f92174-b732-434e-b991-141b5090a94f', 499.99, '2025-05-12'),
('f5959c3c-4801-4b2b-ab44-0c806eb413a4', 599.99, '2025-06-18'),
('584b416b-1b51-48bd-ab9e-7a6a4c9b9792', 149.99, '2025-07-22'),
('0fb94eb1-379b-45b9-a137-aa7fc5ad6368', 399.99, '2025-08-30'),
('13045f03-5a76-4260-8fa2-831995f7671a', 89.99, '2025-09-14'),
('c333ef40-1663-47d1-b4ef-1ac7a9e0eb71', 49.99, '2025-10-01');

insert into users (users_account, users_password, staff_id) VALUES
('james.miller', 'hashed_password_1', '16497cfe-d778-4501-8118-c506560bf47e'),
('olivia.brown', 'hashed_password_2', 'e34ac136-7d00-46f9-bbf8-3b08101c1440'),
('ethan.wilson', 'hashed_password_3', '70fa164a-fa58-4232-8cac-4b42714662a8'),
('sophia.taylor', 'hashed_password_4', '76df5138-6587-41ad-aa57-3d8dca96698e'),
('liam.anderson', 'hashed_password_5', '7f8db744-3ed9-4324-a999-672155e4df35'),
('noah.thompson', 'hashed_password_6', 'd68462cf-5414-4c4c-9568-0ee8f7e04ff7'),
('emma.harris', 'hashed_password_7', '7a32e08f-ac3e-4751-b718-2cfc740c804f'),
('daniel.martinez', 'hashed_password_8', 'efa7a1be-5103-4ea4-a7b8-bf59e2064f6c');

insert into orders (customer_id, users_id, orders_date, orders_total, status_id) VALUES
('d3840fc9-0d38-456e-baf3-49ba635e9466', '1746ba61-3c26-4125-9c66-ce6f9677cef3', '2025-01-20', 1299.98, '30206c49-4f08-4db4-bd97-72c5df53f03b'),
('a8a4d502-c5bc-4cf6-8a55-40407be4e63a', '8139c302-6131-4063-85e0-10fca698495b', '2025-02-25', 899.97, '3c8de017-0587-41fc-a1f0-b1d3eeffc708'),
('fba8b4c0-db71-49eb-8377-9ab4f683b53d', 'f171468d-758d-4bac-ab12-531510f6df57', '2025-03-15', 299.97, '9d6a012d-c59a-458b-8895-cf30cffc5cc4'),
('523bbefb-d412-4193-ba9f-db7f52e9887a', '1746ba61-3c26-4125-9c66-ce6f9677cef3', '2025-04-10', 499.99, '815bd8b8-cb8a-4cfd-b6c1-19f9d38bd3da'),
('194a9a7d-e236-4f51-9bae-4b6694f3bc15', '8139c302-6131-4063-85e0-10fca698495b', '2025-05-18', 699.97, '30206c49-4f08-4db4-bd97-72c5df53f03b'),
('17fa7bf8-4257-436c-9557-e16da709c6b4', 'f171468d-758d-4bac-ab12-531510f6df57', '2025-06-22', 1599.98, '3c8de017-0587-41fc-a1f0-b1d3eeffc708'),
('bf9e59c8-7e7f-47c4-85f2-0945032e520a', '1746ba61-3c26-4125-9c66-ce6f9677cef3', '2025-07-28', 199.99, '9d6a012d-c59a-458b-8895-cf30cffc5cc4'),
('645e177c-8815-4244-a874-d10550a64844', '8139c302-6131-4063-85e0-10fca698495b', '2025-08-05', 399.99, '815bd8b8-cb8a-4cfd-b6c1-19f9d38bd3da');

INSERT INTO item (orders_id, product_id, item_quantity, item_price) VALUES
('72f57024-1f84-41f9-af5f-7fc3e5baf8c2', '03b4aa18-6462-4af1-b727-97364244893c', 1, 999.99),
('72f57024-1f84-41f9-af5f-7fc3e5baf8c2', '4e14ea35-f250-4e8f-940b-0149d156699b', 1, 299.99),
('fd586e98-0ae1-4b23-b02e-6fe1bac68314', '2a18d461-5f4c-4cc5-b041-224ce76fc240', 1, 799.99),
('fd586e98-0ae1-4b23-b02e-6fe1bac68314', 'c333ef40-1663-47d1-b4ef-1ac7a9e0eb71', 2, 49.99),
('f09839fe-49fa-4036-b768-c67dc11f75e6', 'ebb53f41-cf0f-4502-be3a-7776f515512a', 1, 199.99),
('f09839fe-49fa-4036-b768-c67dc11f75e6', 'c333ef40-1663-47d1-b4ef-1ac7a9e0eb71', 2, 49.99),
('08a46cca-d89a-42ed-bc3a-dccd5d0daf87', '95f92174-b732-434e-b991-141b5090a94f', 1, 499.99),
('f081a9c7-6b71-42b9-a45f-7f5701f58eeb', 'f5959c3c-4801-4b2b-ab44-0c806eb413a4', 1, 599.99),
('f081a9c7-6b71-42b9-a45f-7f5701f58eeb', 'c333ef40-1663-47d1-b4ef-1ac7a9e0eb71', 2, 49.99),
('696f7359-aea7-44cf-8351-525560d120bc', '03b4aa18-6462-4af1-b727-97364244893c', 1, 999.99),
('696f7359-aea7-44cf-8351-525560d120bc', 'f5959c3c-4801-4b2b-ab44-0c806eb413a4', 1, 599.99),
('85ab2015-9638-4ae5-a8b3-9bfc905849b8', 'ebb53f41-cf0f-4502-be3a-7776f515512a', 1, 199.99),
('c90bcffd-aef1-494e-8227-8861bc990724', '0fb94eb1-379b-45b9-a137-aa7fc5ad6368', 1, 399.99);