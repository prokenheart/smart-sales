import {
  Box,
  Dialog,
  DialogContent,
  DialogTitle,
  DialogActions,
  Button,
} from "@mui/material";
import type { Dispatch, SetStateAction } from "react";
import CustomerSelect from "./CustomerSelect";
import type { Customer } from "../types/order";
import type { Item } from "../types/item";
import { useState } from "react";
import OrderItemsTable from "./OrderItemsTable";
import CreateOrder from "./CreateOrder";

export default function OrderForm({
  open,
  setOpen,
  mode,
  setIsPosted,
}: Readonly<{
  open: boolean;
  setOpen: Dispatch<SetStateAction<boolean>>;
  mode: "create" | "update" | undefined;
  setIsPosted: Dispatch<SetStateAction<boolean>>;
}>) {
  const [selectedCustomer, setSelectedCustomer] = useState<
    Customer | undefined
  >();
  const [selectedItems, setSelectedItems] = useState<Item[]>([]);


  const handleCancel = () => {
    setOpen(false);
    setSelectedCustomer(undefined);
    setSelectedItems([]);
  };

  return (
    <Dialog
      open={open}
      onClose={() => setOpen(false)}
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
            <CustomerSelect
              selectedCustomer={selectedCustomer}
              setSelectedCustomer={setSelectedCustomer}
            />
            <OrderItemsTable
              items={[]}
              selectedItems={selectedItems}
              itemMode="edit"
              setSelectedItems={setSelectedItems}
            />
          </DialogContent>
          <DialogActions>
            {selectedCustomer && selectedItems.length > 0 && (
              <CreateOrder customer={selectedCustomer} items={selectedItems} setIsPosted={setIsPosted}/>
            )}

            <Button color="error" onClick={handleCancel}>
              Cancel
            </Button>
          </DialogActions>
        </Box>
      </Box>
    </Dialog>
  );
}
