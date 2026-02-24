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
import { useState, Fragment, useEffect } from "react";
import type { ReactElement, Dispatch, SetStateAction } from "react";
import OrderForm from "./OrderForm";
import type { Order } from "../types/order";
import { UpdateTableContext } from "../context/UpdateTableContext";

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

const OrdersTable = ({
  orders,
  totalOrders,
  currentPage,
  ordersPerPage,
  setOrders,
}: Readonly<{
  orders: Order[];
  totalOrders: number;
  currentPage: number;
  ordersPerPage: number;
  setOrders: Dispatch<SetStateAction<Order[]>>;
}>): ReactElement => {
  const [expandedOrderId, setExpandedOrderId] = useState<string | undefined>(
    undefined
  );

  const [openOrderForm, setOpenOrderForm] = useState<boolean>(false);

  const [updatedOrder, setUpdatedOrder] = useState<Order>();

  useEffect(() => {
    if (updatedOrder != undefined) {
      setOpenOrderForm(false);
      setOrders((prev) =>
        prev.map((o) => (o.orderId === updatedOrder.orderId ? updatedOrder : o))
      );
      setUpdatedOrder(undefined);
    }
  }, [updatedOrder]);

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
          <col style={{ width: "15%" }} />
          <col style={{ width: "15%" }} />
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
            <TableCell>Attachment</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {orders.map((order, index) => {
            const isExpanded = expandedOrderId === order.orderId;
            return (
              <Fragment key={order.orderId}>
                <TableRow
                  key={order.orderId}
                  hover
                  onClick={() =>
                    setExpandedOrderId(isExpanded ? undefined : order.orderId)
                  }
                >
                  <TableCell>
                    {ordersPerPage * ((currentPage ?? 0) - 1) + index + 1}
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
                  <TableCell>{Number(order.orderTotal).toFixed(2)}</TableCell>
                  <TableCell
                    sx={{
                      fontWeight: 600,
                      color: getStatusColor(order.status.statusCode),
                    }}
                  >
                    {order.status.statusCode}
                  </TableCell>
                  <TableCell>
                    {new Date(order.orderDate).toLocaleString()}
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
                    colSpan={8}
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
                        <Stack
                          direction="row"
                          justifyContent="center"
                          spacing={4}
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
                              {Number(order.orderTotal).toFixed(2)}
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
                        </Stack>

                        <Box sx={{ mt: 2 }}>
                          <Stack direction="row" spacing={2}>
                            <Button
                              variant="contained"
                              onClick={(e) => {
                                e.stopPropagation();
                                setOpenOrderForm(true);
                              }}
                            >
                              Update
                            </Button>

                            <UpdateTableContext.Provider
                              value={{ setUpdatedOrder }}
                            >
                              <OrderForm
                                open={openOrderForm}
                                setOpen={setOpenOrderForm}
                                mode="update"
                                order={order}
                              />
                            </UpdateTableContext.Provider>

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
                          </Stack>
                        </Box>
                      </Box>
                    </Collapse>
                  </TableCell>
                </TableRow>
              </Fragment>
            );
          })}
        </TableBody>
        <TableFooter>
          <TableRow>
            <TableCell
              colSpan={8}
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
};

export default OrdersTable;
