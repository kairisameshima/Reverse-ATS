'use client'

import React from 'react'
import { useApplicationContext } from './ApplicationContext'
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts"
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"
import { CardContent } from "@/components/ui/card"

export default function ApplicationChartComponent() {
  const { prepareChartData } = useApplicationContext()

  return (
    <CardContent>
      <ChartContainer
        config={{
          RecruiterContact: {
            label: "Recruiter Contact",
            color: "hsl(var(--chart-1))",
          },
          PhoneInterview: {
            label: "Phone Interview",
            color: "hsl(var(--chart-2))",
          },
          TechnicalInterview: {
            label: "Technical Interview",
            color: "hsl(var(--chart-3))",
          },
          OnsiteInterview: {
            label: "Onsite Interview",
            color: "hsl(var(--chart-4))",
          },
          Offer: {
            label: "Offer",
            color: "hsl(var(--chart-5))",
          },
        }}
        className="h-[300px]"
      >
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={prepareChartData()}>
            <XAxis dataKey="date" />
            <YAxis />
            <ChartTooltip content={<ChartTooltipContent />} />
            <Bar dataKey="RecruiterContact" stackId="a" fill="var(--color-RecruiterContact)" />
            <Bar dataKey="PhoneInterview" stackId="a" fill="var(--color-PhoneInterview)" />
            <Bar dataKey="TechnicalInterview" stackId="a" fill="var(--color-TechnicalInterview)" />
            <Bar dataKey="OnsiteInterview" stackId="a" fill="var(--color-OnsiteInterview)" />
            <Bar dataKey="Offer" stackId="a" fill="var(--color-Offer)" />
          </BarChart>
        </ResponsiveContainer>
      </ChartContainer>
    </CardContent>
  )
}