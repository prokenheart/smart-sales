import type { ReactElement } from "react";
import { LineChart, Tooltip, Line, XAxis, YAxis } from "recharts";
import type { YAxisProps } from "recharts";
import { useTheme } from "@mui/material/styles";

type ChartData = {
  key: string;
  value: number;
};

const CHAR_PIXEL_WIDTH = 8;
const Y_AXIS_PADDING = 20;

export const CustomLineChart = ({
  data,
  yAxisFormatter,
}: Readonly<{
  data: ChartData[];
  yAxisFormatter: YAxisProps["tickFormatter"];
}>): ReactElement => {
  const theme = useTheme();

  const getYAxisWidth = (data: { value: number }[]) => {
    const maxLength = Math.max(...data.map((d) => d.value.toFixed(0).toString().length), 0);
    console.log("Max length of Y-axis labels:", maxLength*CHAR_PIXEL_WIDTH);
    return maxLength * CHAR_PIXEL_WIDTH + Y_AXIS_PADDING;
  };

  return (
    <LineChart width={500} height={300} data={data}>
      <YAxis tickFormatter={yAxisFormatter} width={getYAxisWidth(data)} allowDecimals={false} />
      <XAxis dataKey="key" />

      <Tooltip />
      <Line
        type="monotone"
        dataKey="value"
        stroke={theme.palette.primary.main}
        strokeWidth={2}
        dot={false}
      />
    </LineChart>
  );
};
