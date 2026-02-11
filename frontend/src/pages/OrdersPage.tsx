import {
  Box,
  Table,
  TableHead,
  TableBody,
  TableCell,
  TableRow,
  TableFooter,
  Typography,
  Button,
  Collapse,
  Stack,
} from "@mui/material";
import { useEffect, useState } from "react";
import axios from "axios";
import type { ReactElement, Dispatch, SetStateAction } from "react";

type Status = {
  statusId: string;
  statusCode: string;
};

type Customer = {
  customerId: string;
  customerName: string;
  customerPhone: string;
  customerEmail: string;
};

type User = {
  userId: string;
  userName: string;
};

type Order = {
  orderId: string;
  orderTotal: string;
  orderDate: string;
  orderAttachment: string | null;
  updatedAt: string;
  status: Status;
  customer: Customer;
  user: User;
};

type OrdersResponse = {
  orders: Order[];
  prevCursorDate: string | null;
  prevCursorId: string | null;
  nextCursorDate: string | null;
  nextCursorId: string | null;
  totalPages: number;
  currentPage: number;
  totalOrders: number;
};

function getStatusColor(statusCode: string): string {
  switch (statusCode) {
    case "PENDING":
      return "goldenrod";
    case "PAID":
      return "dodgerblue";
    case "DELIVERED":
      return "green";
    case "CANCELLED":
      return "red";
    default:
      return "gray";
  }
}

function ViewOrderItems({ orderId }: Readonly<{ orderId: string }>) {

  useEffect(() => {
    
  })

  return (
    <Button
      variant="text"
      onClick={(e) => {
        e.stopPropagation();
        console.log("View detail", orderId);
      }}
    >
      View Detail
    </Button>
  );
}

function OrdersTable({
  orders,
  totalOrders,
  currentPage,
}: Readonly<{
  orders: Order[];
  totalOrders: number | undefined;
  currentPage: number | undefined;
}>): ReactElement {
  const [expandedOrderId, setExpandedOrderId] = useState<string | undefined>(
    undefined
  );

  return (
    <Box
      sx={{
        height: "450px",
        overflow: "auto",
        border: "1px solid #ddd",
        borderRadius: 2,
      }}
    >
      <Table
        stickyHeader
        sx={{ tableLayout: "fixed", width: "100%", borderCollapse: "collapse" }}
      >
        <colgroup>
          <col style={{ width: "5%" }} />
          <col style={{ width: "15%" }} />
          <col style={{ width: "15%" }} />
          <col style={{ width: "15%" }} />
          <col style={{ width: "10%" }} />
          <col style={{ width: "10%" }} />
          <col style={{ width: "10%" }} />
          <col style={{ width: "10%" }} />
          <col style={{ width: "10%" }} />
        </colgroup>
        <TableHead>
          <TableRow>
            <TableCell>No.</TableCell>
            <TableCell>Order ID</TableCell>
            <TableCell>Customer</TableCell>
            <TableCell>User</TableCell>
            <TableCell>Order Total</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>Order Date</TableCell>
            <TableCell>Updated At</TableCell>
            <TableCell>Attachment</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {orders.map((order, index) => {
            const isExpanded = expandedOrderId === order.orderId;
            return (
              <>
                <TableRow
                  key={order.orderId}
                  hover
                  onClick={() =>
                    setExpandedOrderId(isExpanded ? undefined : order.orderId)
                  }
                >
                  <TableCell>
                    {orders.length * ((currentPage ?? 0) - 1) + index + 1}
                  </TableCell>
                  <TableCell
                    sx={{
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                      whiteSpace: "nowrap",
                    }}
                  >
                    {order.orderId}
                  </TableCell>
                  <TableCell>{order.customer.customerName}</TableCell>
                  <TableCell>{order.user.userName}</TableCell>
                  <TableCell>{order.orderTotal}</TableCell>
                  <TableCell
                    sx={{
                      fontWeight: 600,
                      color: getStatusColor(order.status.statusCode),
                    }}
                  >
                    {order.status.statusCode}
                  </TableCell>
                  <TableCell>
                    {new Date(order.orderDate).toLocaleDateString()}
                  </TableCell>
                  <TableCell>
                    {new Date(order.updatedAt).toLocaleDateString()}
                  </TableCell>
                  <TableCell
                    sx={{
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                      whiteSpace: "nowrap",
                    }}
                  >
                    {order.orderAttachment}
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell
                    colSpan={9}
                    sx={{
                      padding: 0,
                      borderBottom: isExpanded ? "1px solid #ddd" : "none",
                    }}
                  >
                    <Collapse in={isExpanded} timeout="auto" unmountOnExit>
                      <Box sx={{ p: 2, backgroundColor: "#fafafa" }}>
                        <Typography variant="h6" sx={{ mb: 2 }}>
                          Order Detail
                        </Typography>
                        <Box
                          sx={{
                            display: "flex",
                            justifyContent: "space-between",
                            gap: 4,
                          }}
                        >
                          <Box sx={{ flex: 1 }}>
                            <Typography variant="body2">
                              <Typography
                                variant="body2"
                                component="span"
                                sx={{ fontWeight: 600 }}
                              >
                                Order ID:
                              </Typography>{" "}
                              {order.orderId}
                            </Typography>

                            <Typography variant="body2">
                              <Typography
                                variant="body2"
                                component="span"
                                sx={{ fontWeight: 600 }}
                              >
                                Customer Phone:
                              </Typography>{" "}
                              {order.customer.customerPhone}
                            </Typography>

                            <Typography variant="body2">
                              <Typography
                                variant="body2"
                                component="span"
                                sx={{ fontWeight: 600 }}
                              >
                                Customer Email:
                              </Typography>{" "}
                              {order.customer.customerEmail}
                            </Typography>
                          </Box>

                          <Box sx={{ flex: 1 }}>
                            <Typography variant="body2">
                              <Typography
                                variant="body2"
                                component="span"
                                sx={{ fontWeight: 600 }}
                              >
                                Total:
                              </Typography>{" "}
                              {order.orderTotal}
                            </Typography>

                            <Typography variant="body2">
                              <Typography
                                variant="body2"
                                component="span"
                                sx={{ fontWeight: 600 }}
                              >
                                Status:
                              </Typography>{" "}
                              {order.status.statusCode}
                            </Typography>

                            <Typography variant="body2">
                              <Typography
                                variant="body2"
                                component="span"
                                sx={{ fontWeight: 600 }}
                              >
                                Attachment:
                              </Typography>{" "}
                              {order.orderAttachment ?? "None"}
                            </Typography>
                          </Box>
                        </Box>

                        <Box sx={{ mt: 2 }}>
                          <Stack direction="row" spacing={2}>
                            <Button
                              variant="contained"
                              onClick={(e) => {
                                e.stopPropagation();
                                console.log("Update order", order.orderId);
                              }}
                            >
                              Update
                            </Button>

                            <Button
                              variant="outlined"
                              color="warning"
                              onClick={(e) => {
                                e.stopPropagation();
                                console.log("Change status", order.orderId);
                              }}
                            >
                              Change Status
                            </Button>

                            <ViewOrderItems orderId={order.orderId} />
                          </Stack>
                        </Box>
                      </Box>
                    </Collapse>
                  </TableCell>
                </TableRow>
              </>
            );
          })}
        </TableBody>
        <TableFooter>
          <TableRow>
            <TableCell
              colSpan={9}
              sx={{
                position: "sticky",
                bottom: 0,
                backgroundColor: "white",
                fontWeight: 600,
                zIndex: 1,
                borderTop: "1px solid #ddd",
                borderBottom: "0px",
              }}
            >
              Showing {orders.length} of {totalOrders} orders
            </TableCell>
          </TableRow>
        </TableFooter>
      </Table>
    </Box>
  );
}

function OrdersNumberPagination({
  currentPage,
  totalPages,
  setPage,
  setCurrentPage,
}: Readonly<{
  currentPage: number;
  totalPages: number;
  setPage: Dispatch<SetStateAction<number | undefined>>;
  setCurrentPage: Dispatch<SetStateAction<number>>;
}>): ReactElement {
  const pages = Array.from({ length: totalPages }, (_, i) => i + 1);

  const handlePageNumberPagination = (page: number) => {
    setPage(page);
    setCurrentPage(page);
  };

  return (
    <Box sx={{ display: "flex", gap: 1 }}>
      {pages.map((page) => (
        <Button
          key={page}
          variant={page === currentPage ? "contained" : "text"}
          onClick={() => handlePageNumberPagination(page)}
        >
          {page}
        </Button>
      ))}
    </Box>
  );
}

function OrdersPagination({
  currentPage,
  totalPages,
  setPage,
  prevCursorDate,
  prevCursorId,
  nextCursorDate,
  nextCursorId,
  setCursorDate,
  setCursorId,
  setDirection,
  setCurrentPage,
}: Readonly<{
  currentPage: number;
  totalPages: number;
  setPage: Dispatch<SetStateAction<number | undefined>>;
  prevCursorDate: string | undefined;
  prevCursorId: string | undefined;
  nextCursorDate: string | undefined;
  nextCursorId: string | undefined;
  setCursorDate: Dispatch<SetStateAction<string | undefined>>;
  setCursorId: Dispatch<SetStateAction<string | undefined>>;
  setDirection: Dispatch<SetStateAction<string | undefined>>;
  setCurrentPage: Dispatch<SetStateAction<number>>;
}>): ReactElement {
  const handleCursorPagination = (direction: string) => {
    setDirection(direction);
    if (direction == "prev") {
      setCursorDate(prevCursorDate);
      setCursorId(prevCursorId);
      setCurrentPage(currentPage - 1);
    } else if (direction == "next") {
      setCursorDate(nextCursorDate);
      setCursorId(nextCursorId);
      setCurrentPage(currentPage + 1);
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        gap: "1",
      }}
    >
      <Button
        disabled={!prevCursorDate}
        onClick={() => handleCursorPagination("prev")}
      >
        {"<"}
      </Button>
      <OrdersNumberPagination
        currentPage={currentPage}
        totalPages={totalPages}
        setPage={setPage}
        setCurrentPage={setCurrentPage}
      />
      <Button
        disabled={!nextCursorDate}
        onClick={() => handleCursorPagination("next")}
      >
        {">"}
      </Button>
    </Box>
  );
}

export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [prevCursorDate, setPrevCursorDate] = useState<string>();
  const [prevCursorId, setPrevCursorId] = useState<string>();
  const [nextCursorDate, setNextCursorDate] = useState<string>();
  const [nextCursorId, setNextCursorId] = useState<string>();
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [totalOrders, setTotalOrders] = useState<number>(0);

  const [cursorDate, setCursorDate] = useState<string>();
  const [cursorId, setCursorId] = useState<string>();
  const [direction, setDirection] = useState<string>();
  const [page, setPage] = useState<number>();

  useEffect(() => {
    (async () => {
      try {
        const res = await axios.get<OrdersResponse>(
          "https://jw2lw7o6pi.execute-api.ap-southeast-2.amazonaws.com/Prod/orders",
          {
            params: {
              page: page,
              cursorDate: cursorDate,
              cursorId: cursorId,
              direction: direction,
            },
          }
        );
        console.log(currentPage, page, cursorDate);
        setOrders(res.data.orders);
        setPrevCursorDate(res.data.prevCursorDate ?? undefined);
        setPrevCursorId(res.data.prevCursorId ?? undefined);
        setNextCursorDate(res.data.nextCursorDate ?? undefined);
        setNextCursorId(res.data.nextCursorId ?? undefined);
        setTotalPages(res.data.totalPages);
        setTotalOrders(res.data.totalOrders);

        setCursorDate(undefined);
        setCursorId(undefined);
        setDirection(undefined);
        setPage(undefined);
      } catch (err) {
        console.error("Error fetching orders:", err);
      }
    })();
  }, [currentPage]);

  return (
    <Box>
      <Typography>Orders Page</Typography>
      <OrdersTable
        orders={orders}
        totalOrders={totalOrders}
        currentPage={currentPage}
      />
      <OrdersPagination
        currentPage={currentPage}
        totalPages={totalPages}
        setPage={setPage}
        prevCursorDate={prevCursorDate}
        prevCursorId={prevCursorId}
        nextCursorDate={nextCursorDate}
        nextCursorId={nextCursorId}
        setCursorDate={setCursorDate}
        setCursorId={setCursorId}
        setDirection={setDirection}
        setCurrentPage={setCurrentPage}
      />
    </Box>
  );
}
