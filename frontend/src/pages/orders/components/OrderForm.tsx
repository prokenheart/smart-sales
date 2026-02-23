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
import OrderItemsTable from "./OrderItemsTable";
import CreateOrder from "./CreateOrder";
import UpdateOrder from "./UpdateOrder";
import axios from "axios";
import ConfirmClose from "./ConfirmClose";

const API_URL = import.meta.env.VITE_API_URL;

export default function OrderForm({
  open,
  setOpen,
  mode,
  setIsPosted,
  order,
  setUpdatedOrder,
}: Readonly<{
  open: boolean;
  setOpen: Dispatch<SetStateAction<boolean>>;
  mode: "create" | "update" | undefined;
  setIsPosted: Dispatch<SetStateAction<boolean>>;
  order?: Order;
  setUpdatedOrder?: Dispatch<SetStateAction<Order | undefined>>;
}>) {
  const [selectedCustomer, setSelectedCustomer] = useState<
    Customer | undefined
  >();
  const [selectedItems, setSelectedItems] = useState<Item[]>([]);
  const [openConfirm, setOpenConfirm] = useState<boolean>(false);
  const [confirmClose, setConfirmClose] = useState<boolean>(false);

  useEffect(() => {
    if (mode == "update") {
      (async () => {
        try {
          const res = await axios.get<[Item]>(
            `${API_URL}/orders/${order?.orderId}/items`
          );
          setSelectedItems(res.data);
          setSelectedCustomer(order?.customer);
        } catch (err) {
          console.error("Error fetching orders:", err);
        }
      })();
    }
  }, [open]);

  useEffect(()=>{
    if(confirmClose){
      setOpenConfirm(false);
      setConfirmClose(false);
      handleCancel();
    }
  }, [confirmClose])


  const handleCancel = () => {
    setOpen(false);
    setSelectedCustomer(undefined);
    setSelectedItems([]);
  };

  return (
    <>
      <Dialog
        open={open}
        onClose={()=>{setOpenConfirm(true)}}
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

              <OrderItemsTable
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
                  <CreateOrder
                    customer={selectedCustomer}
                    items={selectedItems}
                    setIsPosted={setIsPosted}
                    setSelectedCustomer={setSelectedCustomer}
                    setSelectedItems={setSelectedItems}
                  />
                )}

              {selectedCustomer &&
                selectedItems.length > 0 &&
                mode == "update" && (
                  <UpdateOrder
                    order={order}
                    items={selectedItems}
                    setIsPosted={setIsPosted}
                    setSelectedCustomer={setSelectedCustomer}
                    setSelectedItems={setSelectedItems}
                    setUpdatedOrder={setUpdatedOrder}
                  />
                )}

              <Button color="error" onClick={()=>{setOpenConfirm(true)}}>
                Cancel
              </Button>
            </DialogActions>
          </Box>
        </Box>
      </Dialog>
      <ConfirmClose openConfirm={openConfirm} setOpenConfirm={setOpenConfirm} setConfirmClose={setConfirmClose}/>
    </>
  );
}
