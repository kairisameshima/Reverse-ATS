'use client'

import React, { useState } from 'react'
import { useApplicationContext } from './ApplicationContext'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Trash } from 'lucide-react'
import { format } from 'date-fns'

type ApplicationDetailsProps = {
  applicationId: number
  onClose: () => void
}

export default function ApplicationDetailsComponent({ applicationId, onClose }: ApplicationDetailsProps) {
  const { applications, updateStage, deleteApplication } = useApplicationContext()
  const [isUpdating, setIsUpdating] = useState(false)
  const [isDeleting, setIsDeleting] = useState(false)
  const application = applications.find(app => app.id === applicationId)

  if (!application) return null

  const handleUpdateStage = async (stageName: string, updates: Partial<Stage>) => {
    setIsUpdating(true)
    try {
      await updateStage(applicationId, stageName, updates)
    } catch (error) {
      console.error('Error updating stage:', error)
    } finally {
      setIsUpdating(false)
    }
  }

  const handleDeleteApplication = async () => {
    setIsDeleting(true)
    try {
      await deleteApplication(applicationId)
      onClose()
    } catch (error) {
      console.error('Error deleting application:', error)
    } finally {
      setIsDeleting(false)
    }
  }

  const renderLinearTimeline = () => {
    const allDates = [
      { date: application.dateApplied, event: "Applied" },
      { date: application.dateFirstResponse, event: "First Response" },
      ...application.stages.flatMap(stage => [
        { date: stage.scheduledDate, event: `${stage.name} Scheduled` },
        { date: stage.occurredDate, event: `${stage.name} Occurred` },
      ]),
      { date: application.dateRejected, event: "Rejected" },
    ].filter(item => item.date)

    allDates.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())

    return (
      <div className="space-y-4 mt-4">
        {allDates.map((item, index) => (
          <div key={index} className="flex items-center space-x-4">
            <div className="text-sm font-medium w-24">{format(new Date(item.date), 'MMM dd, yyyy')}</div>
            <div className="w-4 h-4 rounded-full bg-primary"></div>
            <div className="flex-1 text-sm">{item.event}</div>
          </div>
        ))}
      </div>
    )
  }

  return (
    <Card className="mt-4">
      <CardHeader>
        <CardTitle>{application.company} - {application.position}</CardTitle>
        <CardDescription>Application Details</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <Label>Date Applied</Label>
            <Input type="date" value={application.dateApplied} readOnly />
          </div>
          <div>
            <Label>Date of First Response</Label>
            <Input
              type="date"
              value={application.dateFirstResponse}
              onChange={(e) => handleUpdateStage("Applied", { occurredDate: e.target.value })}
              disabled={isUpdating}
            />
          </div>
        </div>
        <Tabs defaultValue={application.stages[0].name}>
          <TabsList className="grid w-full grid-cols-3 lg:grid-cols-6">
            {application.stages.map((stage) => (
              <TabsTrigger key={stage.name} value={stage.name} className="text-xs">
                {stage.name}
              </TabsTrigger>
            ))}
          </TabsList>
          {application.stages.map((stage) => (
            <TabsContent key={stage.name} value={stage.name}>
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor={`${stage.name}-scheduled`}>Scheduled Date</Label>
                  <Input
                    id={`${stage.name}-scheduled`}
                    type="date"
                    value={stage.scheduledDate}
                    onChange={(e) => handleUpdateStage(stage.name, { scheduledDate: e.target.value })}
                    disabled={isUpdating}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor={`${stage.name}-occurred`}>Occurred Date</Label>
                  <Input
                    id={`${stage.name}-occurred`}
                    type="date"
                    value={stage.occurredDate}
                    onChange={(e) => handleUpdateStage(stage.name, { occurredDate: e.target.value })}
                    disabled={isUpdating}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor={`${stage.name}-notes`}>Notes</Label>
                  <Textarea
                    id={`${stage.name}-notes`}
                    value={stage.notes}
                    onChange={(e) => handleUpdateStage(stage.name, { notes: e.target.value })}
                    placeholder="Add your notes here..."
                    disabled={isUpdating}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor={`${stage.name}-status`}>Status</Label>
                  <Select
                    value={stage.status}
                    onValueChange={(value) => handleUpdateStage(stage.name, { status: value as any })}
                    disabled={isUpdating}
                  >
                    <SelectTrigger id={`${stage.name}-status`}>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="pending">Pending</SelectItem>
                      <SelectItem value="scheduled">Scheduled</SelectItem>
                      <SelectItem value="completed">Completed</SelectItem>
                      <SelectItem value="rejected">Rejected</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </TabsContent>
          ))}
        </Tabs>
        {renderLinearTimeline()}
      </CardContent>
      <CardFooter className="flex justify-between">
        <Button variant="destructive" onClick={handleDeleteApplication} disabled={isDeleting}>
          <Trash className="mr-2 h-4 w-4" /> {isDeleting ? 'Deleting...' : 'Delete Application'}
        </Button>
        <Button onClick={onClose}>Close</Button>
      </CardFooter>
    </Card>
  )
}