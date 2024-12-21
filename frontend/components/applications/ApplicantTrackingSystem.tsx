'use client'

import React, { useState } from 'react'
import { useApplicationContext } from './ApplicationContext'
import AddApplicationForm from './AddApplicationForm'
import ApplicationList from './ApplicationList'
import ApplicationDetails from './ApplicationDetails'
import ApplicationChart from './ApplicationChart'
import { Card, CardHeader, CardTitle } from "@/components/ui/card"

export default function ApplicantTrackingSystem() {
  const { applications } = useApplicationContext()
  const [selectedApplication, setSelectedApplication] = useState<number | null>(null)

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Applicant Tracking System</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <AddApplicationForm />
        <ApplicationList 
          applications={applications}
          onSelectApplication={setSelectedApplication}
        />
      </div>
      {selectedApplication !== null && (
        <ApplicationDetails
          applicationId={selectedApplication}
          onClose={() => setSelectedApplication(null)}
        />
      )}
      <Card className="mt-4">
        <CardHeader>
          <CardTitle>Application Rounds Over Time</CardTitle>
        </CardHeader>
        <ApplicationChart />
      </Card>
    </div>
  )
}
