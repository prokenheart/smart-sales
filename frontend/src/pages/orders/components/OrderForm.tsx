import {
  Dialog,
  DialogContent,
  DialogTitle,
  DialogActions,
  Button,
  Typography,
  Stack,
  Box,
} from "@mui/material";
import { useEffect, useMemo, useState } from "react";
import type { Dispatch, ReactElement, SetStateAction } from "react";

import CustomerSelect from "@orders/components/CustomerSelect";
import ItemListTable from "@orders/components/ItemListTable";
import CreateOrderButton from "@orders/components/CreateOrderButton";
import UpdateOrderButton from "@orders/components/UpdateOrderButton";

import type { Customer, Order } from "@orders/types/order";
import type { Item } from "@orders/types/item";

import ConfirmDialog from "@components/ConfirmDialog";

import { getItemList } from "@services/order";

const OrderForm = ({
  isOpen,
  setIsOpen,
  mode,
  order,
}: Readonly<{
  isOpen: boolean;
  setIsOpen: Dispatch<SetStateAction<boolean>>;
  mode: "create" | "update" | undefined;
  order?: Order;
}>): ReactElement => {
  const [selectedCustomer, setSelectedCustomer] = useState<
    Customer | undefined
  >();
  const [selectedItems, setSelectedItems] = useState<Item[]>([]);
  const [isOpenConfirmDialog, setIsOpenConfirmDialog] = useState(false);

  const totalOrder = useMemo(() => {
    const total = selectedItems.reduce((sum, item) => {
      return sum + item.itemQuantity * item.itemPrice;
    }, 0);

    return total.toFixed(2);
  }, [selectedItems]);

  useEffect(() => {
    if (mode == "update") {
      (async () => {
        try {
          if (!order) return;
          const res = await getItemList(order.orderId);
          setSelectedItems(res.data);
          setSelectedCustomer(order.customer);
        } catch (err) {
          console.error("Error fetching orders:", err);
        }
      })();
    }
  }, [open]);

  const handleCancel = () => {
    setIsOpen(false);
    setSelectedCustomer(undefined);
    setSelectedItems([]);
  };

  return (
    <>
      <Dialog
        open={isOpen}
        onClose={() => {
          setIsOpenConfirmDialog(true);
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
        <Stack component="form">
          <DialogTitle
            sx={{
              fontWeight: 600,
              fontSize: "20px",
            }}
          >
            {mode === "create" ? "Create Order" : "Update Order"}
          </DialogTitle>

          <DialogContent
            sx={{
              pt: 1,
            }}
          >
            <Stack spacing={1}>
              <Stack
                direction="row"
                spacing={2}
                alignItems="center"
                justifyContent="space-between"
              >
                <Box width="50%">
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
                </Box>

                <Typography variant="body2">
                  <Typography
                    variant="body2"
                    component="span"
                    sx={{ fontWeight: 600 }}
                  >
                    Total Order:
                  </Typography>{" "}
                  {totalOrder}
                </Typography>
              </Stack>

              <ItemListTable
                items={[]}
                selectedItems={selectedItems}
                itemMode="edit"
                setSelectedItems={setSelectedItems}
              />
            </Stack>
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
                setIsOpenConfirmDialog(true);
              }}
            >
              Cancel
            </Button>
          </DialogActions>
        </Stack>
      </Dialog>
      <ConfirmDialog
        isOpen={isOpenConfirmDialog}
        title="Confirm Close"
        description="Are you sure to exit without saving"
        onCancel={() => setIsOpenConfirmDialog(false)}
        onConfirm={() => {
          setIsOpenConfirmDialog(false);
          handleCancel();
        }}
      />
    </>
  );
};

export default OrderForm;
