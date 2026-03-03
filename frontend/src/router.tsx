import { createBrowserRouter } from "react-router-dom";
import App from "./App";
import Dashboard from "./pages/dashboard/Dashboard";
import OrdersPage from "./pages/orders/OrdersPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { index: true, element: <Dashboard /> },
      { path: "orders", element: <OrdersPage /> },
    ],
  },
]);
