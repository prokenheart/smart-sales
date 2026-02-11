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
import { useState } from "react";
import type { ReactElement } from "react";
import ViewOrderItems from "./ViewOrderItems";
import type { Order } from "../types/order";

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

export default function OrdersTable({
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

                            <ViewOrderItems orderId={order.orderId} status={order.status.statusCode}/>
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
