import { useEffect, useState, type Dispatch, type SetStateAction } from "react";
import type { Item } from "../types/item";
import {
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  Button,
  TextField,
} from "@mui/material";
import { FaRegTrashAlt } from "react-icons/fa";
import { IoIosAdd } from "react-icons/io";
import ProductSelect from "./ProductSelect";
import type { Product } from "../types/product";
import ConfirmDialog from "../../../components/ConfirmDialog";

export default function OrderItemsTable({
  items,
  selectedItems,
  itemMode,
  setSelectedItems,
}: Readonly<{
  items: Item[];
  selectedItems: Item[];
  itemMode: "view" | "edit";
  setSelectedItems: Dispatch<SetStateAction<Item[]>>;
}>) {
  const [newRow, setNewRow] = useState<
    | {
        productId: string;
        productQuantity: number;
      }
    | undefined
  >(undefined);

  const [selectedProduct, setSelectedProduct] = useState<Product>();
  const [openConfirm, setOpenConfirm] = useState<boolean>(false);
  const [deleteId, setDeleteId] = useState<string>();

  const handleChangeQuantity = (productId: string, value: number) => {
    setSelectedItems((prev) =>
      prev.map((item) =>
        item.product.productId === productId
          ? { ...item, itemQuantity: value }
          : item
      )
    );
  };

  const handleDelete = () => {
    setSelectedItems((prev) =>
      prev.filter((item) => item.product.productId !== deleteId)
    );
    setDeleteId(undefined);
  };

  const data = itemMode === "view" ? items : selectedItems;

  useEffect(() => {
    if (selectedProduct != undefined) {
      const newItem: Item = {
        product: {
          productId: selectedProduct.productId,
          productName: selectedProduct.productName,
        },
        itemQuantity: 1,
        itemPrice: selectedProduct.prices[0].priceAmount,
        orderId: undefined,
        updatedAt: undefined,
      };
      setSelectedItems((prev) => [...prev, newItem]);
      setNewRow(undefined);
      setSelectedProduct(undefined);
    }
  }, [selectedProduct]);

  return (
    <>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Product</TableCell>
            <TableCell>Quantity</TableCell>
            <TableCell>Price</TableCell>
            <TableCell>Total</TableCell>
            {itemMode == "edit" && <TableCell></TableCell>}
          </TableRow>
        </TableHead>

        <TableBody>
          {data.map((item) => (
            <TableRow key={item.product.productId}>
              <TableCell>{item.product.productName}</TableCell>
              <TableCell>
                {" "}
                {itemMode === "view" ? (
                  item.itemQuantity
                ) : (
                  <TextField
                    type="number"
                    size="small"
                    value={item.itemQuantity}
                    onChange={(e) => {
                      const value = Number(e.target.value);
                      if (value > 0)
                        handleChangeQuantity(
                          item.product.productId,
                          Number(e.target.value)
                        );
                    }}
                  />
                )}
              </TableCell>
              <TableCell>{item.itemPrice}</TableCell>
              <TableCell>
                {(item.itemQuantity * item.itemPrice).toFixed(2)}
              </TableCell>

              {itemMode == "edit" && (
                <TableCell>
                  <Button
                    color="error"
                    onClick={() => {
                      setDeleteId(item.product.productId);
                      setOpenConfirm(true);
                    }}
                  >
                    <FaRegTrashAlt />
                  </Button>
                </TableCell>
              )}
            </TableRow>
          ))}

          {itemMode == "edit" && newRow && (
            <TableRow>
              <TableCell>
                <ProductSelect
                  selectedProduct={selectedProduct}
                  setSelectedProduct={setSelectedProduct}
                />
              </TableCell>

              <TableCell>
                <TextField
                  type="number"
                  size="small"
                  value={newRow.productQuantity}
                />
              </TableCell>

              <TableCell>-</TableCell>
              <TableCell>-</TableCell>
            </TableRow>
          )}

          {itemMode === "edit" && (
            <TableRow>
              <TableCell colSpan={5} align="center">
                <Button
                  disabled={newRow !== undefined}
                  onClick={() => {
                    setNewRow({
                      productId: "",
                      productQuantity: 1,
                    });
                  }}
                >
                  <IoIosAdd size={30} />
                </Button>
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
      <ConfirmDialog
        open={openConfirm}
        title="Confirm Delete"
        description="Are you sure to delete this"
        onCancel={() => {
          setOpenConfirm(false);
          setDeleteId(undefined);
        }}
        onConfirm={() => {
          setOpenConfirm(false);
          handleDelete();
        }}
      />
    </>
  );
}
