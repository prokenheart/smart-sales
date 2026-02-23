type Status = {
  statusId: string;
  statusCode: string;
};

export type Customer = {
  customerId: string;
  customerName: string;
  customerPhone: string;
  customerEmail: string;
};

type User = {
  userId: string;
  userName: string;
};

export type Order = {
  orderId: string;
  orderTotal: string;
  orderDate: string;
  orderAttachment: string | null;
  updatedAt: string;
  status: Status;
  customer: Customer;
  user: User;
};

export type OrdersResponse = {
  orders: Order[];
  prevCursorDate: string | null;
  prevCursorId: string | null;
  nextCursorDate: string | null;
  nextCursorId: string | null;
  totalPages: number;
  currentPage: number;
  totalOrders: number;
  ordersPerPage: number;
};