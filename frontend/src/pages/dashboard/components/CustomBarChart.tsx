import type { ReactElement } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid } from "recharts";

type ChartData = {
  key: string;
  value: number;
};

const CHAR_PIXEL_WIDTH = 8;
const Y_AXIS_PADDING = 15;

export const CustomBarChart = ({
  data,
}: Readonly<{ data: ChartData[] }>): ReactElement => {
  const top5 = data.slice(0, 5);

  const getYAxisWidth = (data: { key: string }[]) => {
    const maxLength = Math.max(...data.map((d) => d.key.length));
    return maxLength * CHAR_PIXEL_WIDTH + Y_AXIS_PADDING;
  };

  return (
    <BarChart height={300} data={top5} layout="vertical">
      <CartesianGrid strokeDasharray="3 3" />

      <XAxis type="number" tickFormatter={(value) => `$${value}`} />

      <YAxis
        type="category"
        dataKey="key"
        interval={0}
        width={getYAxisWidth(data)}
      />

      <Bar dataKey="value" fill="#f9b17a" />
    </BarChart>
  );
};
