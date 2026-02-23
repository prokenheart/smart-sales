import {
  Box,
  Dialog,
  DialogContent,
  DialogTitle,
  DialogActions,
  Button,
  Typography,
} from "@mui/material";
import type { Dispatch, SetStateAction } from "react";
import CustomerSelect from "./CustomerSelect";
import type { Customer, Order } from "../types/order";
import type { Item } from "../types/item";
import { useEffect, useState } from "react";
import ItemListTable from "./ItemListTable";
import CreateOrderButton from "./CreateOrderButton";
import UpdateOrderButton from "./UpdateOrderButton";
import ConfirmDialog from "../../../components/ConfirmDialog";
import { getItemList } from "../../../services/order";

export default function OrderForm({
  open,
  setOpen,
  mode,
  order,
}: Readonly<{
  open: boolean;
  setOpen: Dispatch<SetStateAction<boolean>>;
  mode: "create" | "update" | undefined;
  order?: Order;
}>) {
  const [selectedCustomer, setSelectedCustomer] = useState<
    Customer | undefined
  >();
  const [selectedItems, setSelectedItems] = useState<Item[]>([]);
  const [openConfirm, setOpenConfirm] = useState<boolean>(false);

  useEffect(() => {
    if (mode == "update") {
      (async () => {
        try {
          if (order != undefined) {
            const res = await getItemList(order.orderId);
            setSelectedItems(res.data);
            setSelectedCustomer(order.customer);
          }
        } catch (err) {
          console.error("Error fetching orders:", err);
        }
      })();
    }
  }, [open]);

  const handleCancel = () => {
    setOpen(false);
    setSelectedCustomer(undefined);
    setSelectedItems([]);
  };

  return (
    <>
      <Dialog
        open={open}
        onClose={() => {
          setOpenConfirm(true);
        }}
        fullWidth
        maxWidth="md"
        sx={{
          "& .MuiDialog-paper": {
            borderRadius: 3,
            p: 1,
          },
        }}
      >
        <Box
          component="form"
          sx={{
            display: "flex",
            flexDirection: "column",
            gap: 0,
          }}
        >
          <DialogTitle
            sx={{
              fontWeight: 600,
              fontSize: "20px",
            }}
          >
            {mode === "create" ? "Create Order" : "Update Order"}
          </DialogTitle>
          <Box>
            <DialogContent
              sx={{
                display: "flex",
                flexDirection: "column",
                gap: 1,
                pt: 1,
              }}
            >
              {mode == "create" && (
                <CustomerSelect
                  selectedCustomer={selectedCustomer}
                  setSelectedCustomer={setSelectedCustomer}
                />
              )}

              {mode == "update" && (
                <Typography variant="body2">
                  <Typography
                    variant="body2"
                    component="span"
                    sx={{ fontWeight: 600 }}
                  >
                    Customer Name:
                  </Typography>{" "}
                  {order?.customer.customerName}
                </Typography>
              )}

              <ItemListTable
                items={[]}
                selectedItems={selectedItems}
                itemMode="edit"
                setSelectedItems={setSelectedItems}
              />
            </DialogContent>
            <DialogActions>
              {selectedCustomer &&
                selectedItems.length > 0 &&
                mode == "create" && (
                  <CreateOrderButton
                    customer={selectedCustomer}
                    items={selectedItems}
                    setSelectedCustomer={setSelectedCustomer}
                    setSelectedItems={setSelectedItems}
                  />
                )}

              {selectedCustomer &&
                selectedItems.length > 0 &&
                mode == "update" && (
                  <UpdateOrderButton
                    order={order}
                    items={selectedItems}
                    setSelectedCustomer={setSelectedCustomer}
                    setSelectedItems={setSelectedItems}
                  />
                )}

              <Button
                color="error"
                onClick={() => {
                  setOpenConfirm(true);
                }}
              >
                Cancel
              </Button>
            </DialogActions>
          </Box>
        </Box>
      </Dialog>
      <ConfirmDialog
        open={openConfirm}
        title="Confirm Close"
        description="Are you sure to exit without saving"
        onCancel={() => setOpenConfirm(false)}
        onConfirm={() => {
          setOpenConfirm(false);
          handleCancel();
        }}
      />
    </>
  );
}
