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

type ResponseData = {
  key: string;
  total: number;
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

const formatters = {
  currency: (value: number | string) => `$${Number(value)}`,
  number: (value: number | string) => String(value),
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

  const mapDailyResponseToChartData  = (data: ResponseData[]): ChartData[] =>
    data.map((item) => {
      const date = new Date(item.key);
      return {
        key: `${date.getDate()}-${date.toLocaleString("en-US", { month: "short" })}`,
        value: item.total,
      };
    });

  const mapMonthlyResponseToChartData = (data: ResponseData[]): ChartData[] =>
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

      const ordersData = mapDailyResponseToChartData (totalOrders);
      const revenueData = mapDailyResponseToChartData (totalRevenue);
      const monthlyRevenueData = mapMonthlyResponseToChartData(monthlyRevenue);
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
            content={formatters.currency(dashboard.revenue.today)}
            chart={
              <CustomLineChart
                data={dashboard.revenue.summary}
                yAxisFormatter={formatters.currency}
              />
            }
          />
          <CustomCard
            title="This Month Revenue"
            content={formatters.currency(dashboard.monthlyRevenue.thisMonth)}
            chart={
              <CustomLineChart
                data={dashboard.monthlyRevenue.summary}
                yAxisFormatter={formatters.currency}
              />
            }
          />
        </Stack>
        <Stack direction={"row"} spacing={2}>
          <CustomCard
            title="New Orders"
            content={formatters.number(dashboard.totalOrders.today)}
            chart={
              <CustomLineChart
                data={dashboard.totalOrders.summary}
                yAxisFormatter={formatters.number}
              />
            }
          />
          <CustomCard
            title="Top Products by Revenue (Last 7 Days)"
            chart={<CustomBarChart data={dashboard.topProductRevenue} />}
            chartHeight={140}
          />
        </Stack>
      </Stack>
    </Box>
  );
};

export default Dashboard;
