import { Button, Typography, Stack } from "@mui/material";
import { useEffect, useState, type ReactElement } from "react";
import OrdersTable from "./components/OrdersTable";
import OrdersPagination from "./components/OrdersPagination";
import type { Order } from "./types/order";
import OrderForm from "./components/OrderForm";
import SearchBox from "./components/SearchBox";
import { getOrders } from "../../services/order";
import { OrderRefreshContext } from "./context/OrderRefreshContext";
import type { CursorResponse, CursorState } from "./types/cursor";

const OrdersPage = (): ReactElement => {
  const [orders, setOrders] = useState<Order[]>([]);

  const [cursorResponse, setCursorResponse] = useState<CursorResponse>();

  const [currentPage, setCurrentPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  
  const [totalOrders, setTotalOrders] = useState<number>(0);
  const [ordersPerPage, setOrdersPerPage] = useState<number>(1);

  const [page, setPage] = useState<number>();

  const [cursorState, setCursorState] = useState<CursorState>();

  const [open, setOpen] = useState<boolean>(false);

  const [shouldRefreshOrder, setShouldRefreshOrder] = useState<boolean>(false);

  const [search, setSearch] = useState<string>("");

  const handleCreateOrder = () => {
    setOpen(true);
  };

  const fetchOrders = async () => {
    const res = await getOrders(
      page,
      cursorState?.cursor.cursorDate,
      cursorState?.cursor.cursorId,
      cursorState?.direction,
      search
    );

    setOrders(res.data.orders);
    setCursorResponse({
      prev: {
        cursorDate: res.data.prevCursorDate ?? undefined,
        cursorId: res.data.prevCursorId ?? undefined
      },
      next: {
        cursorDate: res.data.nextCursorDate ?? undefined,
        cursorId: res.data.nextCursorId ?? undefined
      }
    });
    setTotalPages(res.data.totalPages);
    setTotalOrders(res.data.totalOrders);
    setOrdersPerPage(res.data.ordersPerPage);

    setCursorState(undefined);
    setPage(undefined);
  };

  useEffect(() => {
    fetchOrders();
  }, [currentPage]);

  useEffect(() => {
    if (currentPage === 1) fetchOrders();
    else setCurrentPage(1);
  }, [search]);

  useEffect(() => {
    if (shouldRefreshOrder) {
      setOpen(false);
      setShouldRefreshOrder(false);
      if (currentPage === 1) fetchOrders();
      else setCurrentPage(1);
    }
  }, [shouldRefreshOrder]);

  return (
    <>
      <Stack
        direction="row"
        justifyContent="space-between"
        alignItems="center"
        mb={2}
      >
        <Typography variant="h5">Orders</Typography>

        <Stack direction="row" spacing={2} alignItems="center">
          <SearchBox value={search} onChange={setSearch} delay={500} />
          <Button variant="contained" onClick={handleCreateOrder}>
            Add Order
          </Button>
        </Stack>

        <OrderRefreshContext.Provider value={{ setShouldRefreshOrder }}>
          <OrderForm open={open} setOpen={setOpen} mode="create" />
        </OrderRefreshContext.Provider>
      </Stack>

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
        cursorResponse={cursorResponse}
        setCursorState={setCursorState}
        setCurrentPage={setCurrentPage}
      />
    </>
  );
};

export default OrdersPage;
