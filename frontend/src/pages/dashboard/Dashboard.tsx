import { Box, Stack, Typography } from "@mui/material";
import { useEffect, type ReactElement, useState } from "react";

import CustomCard from "@dashboard/components/CustomCard";
import { CustomLineChart } from "@dashboard/components/CustomLineChart";
import { CustomBarChart } from "@dashboard/components/CustomBarChart";

import { getDashboardSummary } from "@services/dashboard";

type ChartData = {
  key: string;
  value: number;
};

type DashboardState = {
  totalOrders: {
    summary: ChartData[];
    today: number;
  };
  revenue: {
    summary: ChartData[];
    today: number;
  };
  monthlyRevenue: {
    summary: ChartData[];
    thisMonth: number;
  };
  topProductRevenue: ChartData[];
};

const Dashboard = (): ReactElement => {
  const [dashboard, setDashboard] = useState<DashboardState>({
    totalOrders: {
      summary: [],
      today: 0,
    },
    revenue: {
      summary: [],
      today: 0,
    },
    monthlyRevenue: {
      summary: [],
      thisMonth: 0,
    },
    topProductRevenue: [],
  });

  const mapData = (data: any[]) =>
    data.map((item) => {
      const d = new Date(item.key);
      return {
        key: `${d.getDate()}/${d.getMonth() + 1}`,
        value: item.total,
      };
    });

  const mapMonthData = (data: any[]) =>
    data.map((item) => {
      const [year, month] = item.key.split("-");
      const date = new Date(Number(year), Number(month) - 1);

      return {
        key: date.toLocaleString("en-US", { month: "short" }),
        value: item.total,
      };
    });

  const fetchDashboardData = async () => {
    try {
      const { totalOrders, totalRevenue, monthlyRevenue, topProducts } =
        await getDashboardSummary();

      const ordersData = mapData(totalOrders);
      const revenueData = mapData(totalRevenue);
      const monthlyRevenueData = mapMonthData(monthlyRevenue);
      const topProductRevenueData = topProducts.map((item) => ({
        key: item.key,
        value: item.total,
      }));

      setDashboard({
        totalOrders: {
          summary: ordersData,
          today: ordersData.at(-1)?.value ?? 0,
        },
        revenue: {
          summary: revenueData,
          today: revenueData.at(-1)?.value ?? 0,
        },
        monthlyRevenue: {
          summary: monthlyRevenueData,
          thisMonth: monthlyRevenueData.at(-1)?.value ?? 0,
        },
        topProductRevenue: topProductRevenueData,
      });
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  return (
    <Box>
      <Typography variant="h5" mb={3} fontWeight={600}>
        See what happen today
      </Typography>

      <Stack spacing={2}>
        <Stack direction={"row"} spacing={2}>
          <CustomCard
            title="Today Revenue"
            content={"$" + dashboard.revenue.today}
            chart={<CustomLineChart data={dashboard.revenue.summary} />}
          />
          <CustomCard
            title="This Month Revenue"
            content={"$" + dashboard.monthlyRevenue.thisMonth}
            chart={<CustomLineChart data={dashboard.monthlyRevenue.summary} />}
          />
        </Stack>
        <Stack direction={"row"} spacing={2}>
          <CustomCard
            title="New Orders"
            content={dashboard.totalOrders.today.toString()}
            chart={<CustomLineChart data={dashboard.totalOrders.summary} />}
          />
          <CustomCard
            title="Top Product Revenue"
            chart={<CustomBarChart data={dashboard.topProductRevenue} />}
            chartHeight={140}
          />
        </Stack>
      </Stack>
    </Box>
  );
};

export default Dashboard;
