import {
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
  Tooltip,
  Box,
} from "@mui/material";
import axios from "axios";
import { useEffect, useState } from "react";
import type { ReactElement, Dispatch, SetStateAction } from "react";
import OrderItemsTable from "./OrderItemsTable";
import UpdateOrderItems from "./UpdateOrderItems";
import type { Item } from "../types/item";

const API_URL = import.meta.env.VITE_API_URL;

function PopUpItemList({
  open,
  setOpen,
  items,
  loading,
  status,
}: Readonly<{
  open: boolean;
  setOpen: Dispatch<SetStateAction<boolean>>;
  items: Item[];
  loading: boolean;
  status: string;
}>): ReactElement {
  const [mode, setMode] = useState<"view" | "edit">("view");
  const [editItems, setEditItems] = useState<Item[]>([]);

  const handleEdit = () => {
    setEditItems(structuredClone(items));
    setMode("edit");
  };

  const handleCancel = () => {
    setEditItems([]);
    setMode("view");
  };

  return (
    <Dialog open={open} onClose={() => setOpen(false)} fullWidth maxWidth="md">
      <DialogTitle>Order Items</DialogTitle>

      <DialogContent>
        {loading ? (
          <CircularProgress />
        ) : (
          <OrderItemsTable items={items} selectedItems={editItems} itemMode={mode} setSelectedItems={setEditItems} />
        )}
      </DialogContent>

      <DialogActions>
        {mode === "view" ? (
          <Tooltip
            title={status !== "PENDING" ? "Can not update this order" : ""}
            arrow
          >
            <Box component="span">
              <Button
                variant="contained"
                onClick={handleEdit}
                disabled={status !== "PENDING"}
              >
                Update Item
              </Button>
            </Box>
          </Tooltip>
        ) : (
          <>
            <UpdateOrderItems editItems={editItems} />

            <Button color="error" onClick={handleCancel}>
              Cancel
            </Button>
          </>
        )}
        <Button onClick={() => setOpen(false)}>Close</Button>
      </DialogActions>
    </Dialog>
  );
}

export default function ViewOrderItems({
  orderId,
  status,
}: Readonly<{ orderId: string; status: string }>): ReactElement {
  const [open, setOpen] = useState<boolean>(false);
  const [items, setItems] = useState<Item[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    if (!open) return;
    (async () => {
      try {
        setLoading(true);
        const res = await axios.get<[Item]>(
          `${API_URL}/orders/${orderId}/items`
        );
        setItems(res.data);
      } catch (err) {
        console.error("Error fetching orders:", err);
      } finally {
        setLoading(false);
      }
    })();
  }, [open, orderId]);

  return (
    <>
      <Button
        variant="text"
        onClick={(e) => {
          e.stopPropagation();
          console.log("View detail", orderId);
          setOpen(true);
        }}
      >
        View Detail
      </Button>
      <PopUpItemList
        open={open}
        setOpen={setOpen}
        items={items}
        loading={loading}
        status={status}
      />
    </>
  );
}
