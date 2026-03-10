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
  CircularProgress,
} from "@mui/material";
import { useState, Fragment, useEffect } from "react";
import type { ReactElement, Dispatch, SetStateAction } from "react";
import { HttpStatusCode } from "axios";
import { useSnackbar } from "notistack";

import OrderForm from "@orders/components/OrderForm";
import AttachmentPreviewButton from "@orders/components/AttachmentPreviewButton";
import AttachmentPreviewDialog from "@orders/components/AttachmentPreviewDialog";

import { UpdateTableContext } from "@orders/context/UpdateTableContext";

import type { Order } from "@orders/types/order";
import { OrderStatus } from "@orders/types/status";

import ConfirmDialog from "@components/ConfirmDialog";

import {
  updateOrderStatus,
  createUploadAttachmentURL,
  uploadAttachment,
  updateAttachmentLink,
} from "@services/order";

import FilePicker from "@orders/components/FilePicker";
import FilePreviewDialog from "@orders/components/FilePreviewDialog";

function getStatusColor(statusCode: string): string {
  switch (statusCode) {
    case OrderStatus.Pending:
      return "goldenrod";
    case OrderStatus.Paid:
      return "dodgerblue";
    case OrderStatus.Delivered:
      return "green";
    case OrderStatus.Cancelled:
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
  isLoading,
}: Readonly<{
  orders: Order[];
  totalOrders: number;
  currentPage: number;
  ordersPerPage: number;
  setOrders: Dispatch<SetStateAction<Order[]>>;
  isLoading: boolean;
}>): ReactElement => {
  const [expandedOrderId, setExpandedOrderId] = useState<string | undefined>(
    undefined
  );

  const [isOpenOrderForm, setIsOpenOrderForm] = useState(false);

  const [updatedOrder, setUpdatedOrder] = useState<Order>();

  const [isOpenViewDialog, setIsOpenViewDialog] = useState(false);
  const [viewURL, setViewURL] = useState<string | null>(null);
  const [isOpenConfirmDialog, setIsOpenConfirmDialog] = useState(false);
  const [selectedOrderId, setSelectedOrderId] = useState<string>();

  const { enqueueSnackbar } = useSnackbar();

  const handleCancelOrder = async (orderId: string) => {
    try {
      const res = await updateOrderStatus(orderId, OrderStatus.Cancelled);
      if (res.status === HttpStatusCode.Ok) {
        setOrders((prev) =>
          prev.map((order) =>
            order.orderId === orderId
              ? {
                  ...order,
                  status: {
                    ...order.status,
                    statusCode: OrderStatus.Cancelled,
                  },
                }
              : order
          )
        );
        enqueueSnackbar("Order cancelled successfully", { variant: "success" });
      }
    } catch (error) {
      console.error("Cancel Order Failed: ", error);
    }
  };

  const handleConfirmCancelOrder = async () => {
    if (!selectedOrderId) return;

    await handleCancelOrder(selectedOrderId);

    setIsOpenConfirmDialog(false);
    setSelectedOrderId(undefined);
  };

  const [uploadOrder, setUploadOrder] = useState<Order>();

  const [file, setFile] = useState<File | null>(null);
  const [isOpenPreviewDialog, setIsOpenPreviewDialog] = useState(false);
  const [previewPickedFileSrc, setPreviewPickedFileSrc] = useState<string>();

  const handleSelect = (file: File, order: Order) => {
    setUploadOrder(order);
    setFile(file);
    setIsOpenPreviewDialog(true);
    if (file) {
      const url = URL.createObjectURL(file);
      setPreviewPickedFileSrc(url);
    }
  };

  const handleCancelUpload = () => {
    setFile(null);
    setIsOpenPreviewDialog(false);
    setPreviewPickedFileSrc(undefined);
  };

  const handleCreateUploadURL = async (order: Order) => {
    try {
      if (!file) return;
      const res = await createUploadAttachmentURL(order.orderId, file.type);
      return res.data;
    } catch (error) {
      console.error("Create pre-signed url failed", error);
    }
  };

  const handleUploadToS3 = async (preSignedUrl: string) => {
    try {
      if (!file) return;
      await uploadAttachment(preSignedUrl, file);
    } catch (error) {
      console.error("Upload file to s3 bucket failed", error);
    }
  };

  const handleUpdateAttachmentLink = async (order: Order, s3Key: string) => {
    try {
      await updateAttachmentLink(order.orderId, s3Key);
    } catch (error) {
      console.error("Upload attachment link to database failed", error);
    }
  };

  const handleUpload = async (order: Order | undefined) => {
    try {
      if (!order) return;
      const { uploadUrl, s3Key } = await handleCreateUploadURL(order);

      await handleUploadToS3(uploadUrl);
      await handleUpdateAttachmentLink(order, s3Key);

      const attachmentUpdatedOrder: Order = {
        ...order,
        orderAttachment: s3Key,
      };

      setUpdatedOrder(attachmentUpdatedOrder);
      enqueueSnackbar("Attachment uploaded successfully", {
        variant: "success",
      });
      setFile(null);
      setIsOpenPreviewDialog(false);
      setPreviewPickedFileSrc(undefined);
    } catch (error) {
      console.error("Upload flow failed", error);
    }
  };

  useEffect(() => {
    if (updatedOrder) {
      setIsOpenOrderForm(false);
      setOrders((prev) =>
        prev.map((o) => (o.orderId === updatedOrder.orderId ? updatedOrder : o))
      );
      setUpdatedOrder(undefined);
      enqueueSnackbar("Order updated successfully", { variant: "success" });
    }
  }, [updatedOrder]);

  return (
    <Box
      sx={{
        maxHeight: "450px",
        overflow: "auto",
        border: "1px solid",
        borderColor: "secondary.main",
        borderRadius: 2,
      }}
    >
      <Table
        stickyHeader
        sx={{
          tableLayout: "fixed",
          width: "100%",
          borderCollapse: "collapse",
          height: "100%",
        }}
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
          {isLoading ? (
            <TableRow>
              <TableCell colSpan={8} align="center">
                <CircularProgress />
              </TableCell>
            </TableRow>
          ) : (
            orders.map((order, index) => {
              const isExpanded = expandedOrderId === order.orderId;
              const isDisabled =
                order.status.statusCode === OrderStatus.Cancelled;
              return (
                <Fragment key={order.orderId}>
                  <TableRow
                    key={order.orderId}
                    onClick={() =>
                      setExpandedOrderId(isExpanded ? undefined : order.orderId)
                    }
                    hover
                    sx={{ height: "70px" }}
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
                    <TableCell>
                      {order.orderAttachment && (
                        <AttachmentPreviewButton
                          orderId={order.orderId}
                          setViewURL={setViewURL}
                          setIsOpenViewDialog={setIsOpenViewDialog}
                        />
                      )}
                    </TableCell>
                  </TableRow>
                  <TableRow
                    sx={{
                      height: isExpanded ? "auto" : 0,
                    }}
                  >
                    <TableCell
                      colSpan={8}
                      sx={{
                        padding: 0,
                        borderBottom: isExpanded ? "1px solid" : "0px",
                        borderColor: "primary.contrastText",
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
                            </Box>
                          </Stack>

                          <Box sx={{ mt: 2 }}>
                            <Stack direction="row" spacing={2}>
                              <Button
                                variant="contained"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  setIsOpenOrderForm(true);
                                }}
                                disabled={isDisabled}
                              >
                                Update
                              </Button>

                              <UpdateTableContext.Provider
                                value={{ setUpdatedOrder }}
                              >
                                <OrderForm
                                  isOpen={isOpenOrderForm}
                                  setIsOpen={setIsOpenOrderForm}
                                  mode="update"
                                  order={order}
                                />
                              </UpdateTableContext.Provider>
                              <Button
                                variant="contained"
                                color="error"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  setIsOpenConfirmDialog(true);
                                  setSelectedOrderId(order.orderId);
                                }}
                                disabled={isDisabled}
                              >
                                Cancel
                              </Button>
                              <FilePicker
                                onSelect={handleSelect}
                                order={order}
                                isDisabled={isDisabled}
                              />
                            </Stack>
                          </Box>
                        </Box>
                      </Collapse>
                    </TableCell>
                  </TableRow>
                </Fragment>
              );
            })
          )}
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
                borderColor: "primary.contrastText",
                borderBottom: "0px",
              }}
            >
              Showing {orders.length} of {totalOrders} orders
            </TableCell>
          </TableRow>
        </TableFooter>
      </Table>

      <AttachmentPreviewDialog
        viewURL={viewURL}
        isOpen={isOpenViewDialog}
        setIsOpen={setIsOpenViewDialog}
        setViewURL={setViewURL}
      />
      <ConfirmDialog
        isOpen={isOpenConfirmDialog}
        title="Cancel Order"
        description="Are you sure to cancel this order?"
        onCancel={() => {
          setIsOpenConfirmDialog(false);
          setSelectedOrderId(undefined);
        }}
        onConfirm={handleConfirmCancelOrder}
      />
      {previewPickedFileSrc && (
        <FilePreviewDialog
          isOpen={isOpenPreviewDialog}
          previewPickedFileSrc={previewPickedFileSrc}
          onCancel={handleCancelUpload}
          onConfirm={() => handleUpload(uploadOrder)}
        />
      )}
    </Box>
  );
};

export default OrdersTable;
