import {
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  CircularProgress,
  TextField,
  Tooltip,
  Box
} from "@mui/material";
import axios from "axios";
import { useEffect, useState } from "react";
import type { ReactElement, Dispatch, SetStateAction } from "react";
import { FaRegTrashAlt } from "react-icons/fa";
import { IoIosAdd } from "react-icons/io";

const API_URL = import.meta.env.VITE_API_URL;

type Product = {
  productId: string;
  productName: string;
};

type Item = {
  product: Product;
  itemQuantity: number;
  itemPrice: number;
  orderId: string;
  updatedAt: string;
};

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

  const handleChangeQuantity = (productId: string, value: number) => {
    setEditItems((prev) =>
      prev.map((item) =>
        item.product.productId === productId
          ? { ...item, itemQuantity: value }
          : item
      )
    );
  };

  const handleDelete = (productId: string) => {
    setEditItems((prev) =>
      prev.filter((item) => item.product.productId !== productId)
    );
  };

  const data = mode === "view" ? items : editItems;
  return (
    <Dialog open={open} onClose={() => setOpen(false)} fullWidth maxWidth="md">
      <DialogTitle>Order Items</DialogTitle>

      <DialogContent>
        {loading ? (
          <CircularProgress />
        ) : (
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Product</TableCell>
                <TableCell>Quantity</TableCell>
                <TableCell>Price</TableCell>
                <TableCell>Total</TableCell>
                {mode == "edit" && <TableCell></TableCell>}
              </TableRow>
            </TableHead>

            <TableBody>
              {data.map((item) => (
                <TableRow key={item.product.productId}>
                  <TableCell>{item.product.productName}</TableCell>
                  <TableCell>
                    {" "}
                    {mode === "view" ? (
                      item.itemQuantity
                    ) : (
                      <TextField
                        type="number"
                        size="small"
                        value={item.itemQuantity}
                        onChange={(e) =>
                          handleChangeQuantity(
                            item.product.productId,
                            Number(e.target.value)
                          )
                        }
                      />
                    )}
                  </TableCell>
                  <TableCell>{item.itemPrice}</TableCell>
                  <TableCell>
                    {(item.itemQuantity * item.itemPrice).toFixed(2)}
                  </TableCell>
                  {mode == "edit" && (
                    <TableCell>
                      <Button
                        color="error"
                        onClick={() => handleDelete(item.product.productId)}
                      >
                        <FaRegTrashAlt />
                      </Button>
                    </TableCell>
                  )}
                </TableRow>
              ))}
              {mode === "edit" && (
                <TableRow>
                  <TableCell colSpan={5} align="center">
                    <Button>
                      <IoIosAdd size={30} />
                    </Button>
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
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
            <Button
              variant="contained"
              onClick={() => {
                console.log("SAVE DATA", editItems);
              }}
            >
              Save
            </Button>

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
