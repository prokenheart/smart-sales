import { Box, Button, Typography } from "@mui/material";
import { useEffect, useState } from "react";
import axios from "axios";
import OrdersTable from "./components/OrdersTable";
import OrdersPagination from "./components/OrdersPagination";
import type { Order } from "./types/order";
import OrderForm from "./components/OrderForm";
import SearchBox from "./components/SearchBox";

const API_URL = import.meta.env.VITE_API_URL;

type OrdersResponse = {
  orders: Order[];
  prevCursorDate: string | null;
  prevCursorId: string | null;
  nextCursorDate: string | null;
  nextCursorId: string | null;
  totalPages: number;
  currentPage: number;
  totalOrders: number;
  ordersPerPage: number;
};

export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [prevCursorDate, setPrevCursorDate] = useState<string>();
  const [prevCursorId, setPrevCursorId] = useState<string>();
  const [nextCursorDate, setNextCursorDate] = useState<string>();
  const [nextCursorId, setNextCursorId] = useState<string>();

  const [currentPage, setCurrentPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [totalOrders, setTotalOrders] = useState<number>(0);
  const [ordersPerPage, setOrdersPerPage] = useState<number>(1);

  const [cursorDate, setCursorDate] = useState<string>();
  const [cursorId, setCursorId] = useState<string>();
  const [direction, setDirection] = useState<"prev" | "next">();
  const [page, setPage] = useState<number>();

  const [open, setOpen] = useState<boolean>(false);

  const [isPosted, setIsPosted] = useState<boolean>(false);

  const [search, setSearch] = useState<string>("");

  const handleCreateOrder = () => {
    setOpen(true);
  };

  const fetchOrders = async () => {
    const res = await axios.get<OrdersResponse>(`${API_URL}/orders`, {
      params: {
        page,
        cursorDate,
        cursorId,
        direction,
        search
      },
    });

    setOrders(res.data.orders);
    setPrevCursorDate(res.data.prevCursorDate ?? undefined);
    setPrevCursorId(res.data.prevCursorId ?? undefined);
    setNextCursorDate(res.data.nextCursorDate ?? undefined);
    setNextCursorId(res.data.nextCursorId ?? undefined);
    setTotalPages(res.data.totalPages);
    setTotalOrders(res.data.totalOrders);
    setOrdersPerPage(res.data.ordersPerPage);

    setCursorDate(undefined);
    setCursorId(undefined);
    setDirection(undefined);
    setPage(undefined);
  };

  useEffect(() => {
    fetchOrders();
  }, [currentPage]);

  useEffect(()=>{
    if (currentPage === 1) fetchOrders();
    else setCurrentPage(1);
  }, [search])

  useEffect(() => {
    if (isPosted) {
      setOpen(false);
      setIsPosted(false);
      if (currentPage === 1) fetchOrders();
      else setCurrentPage(1);
    }
  }, [isPosted]);

  return (
    <Box>
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 2,
        }}
      >
        <Typography variant="h5">Orders</Typography>

        <Box sx={{ display: "flex", gap: 2, alignItems: "center" }}>
          <SearchBox
            value={search}
            onChange={setSearch}
            delay={500}
          />
          <Button variant="contained" onClick={handleCreateOrder}>
            Add Order
          </Button>
        </Box>

        <OrderForm
          open={open}
          setOpen={setOpen}
          mode="create"
          setIsPosted={setIsPosted}
        />
      </Box>

      <OrdersTable
        orders={orders}
        totalOrders={totalOrders}
        currentPage={currentPage}
        ordersPerPage={ordersPerPage}
        setOrders={setOrders}
      />
      <OrdersPagination
        currentPage={currentPage}
        totalPages={totalPages}
        setPage={setPage}
        prevCursorDate={prevCursorDate}
        prevCursorId={prevCursorId}
        nextCursorDate={nextCursorDate}
        nextCursorId={nextCursorId}
        setCursorDate={setCursorDate}
        setCursorId={setCursorId}
        setDirection={setDirection}
        setCurrentPage={setCurrentPage}
      />
    </Box>
  );
}
