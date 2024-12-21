'use client'

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { format } from 'date-fns'
import { Trash } from 'lucide-react'
import { useState } from 'react'
import { useApplicationContext } from './ApplicationContext'

type ApplicationDetailsProps = {
  applicationUuid: string
  onClose: () => void
}

export default function ApplicationDetails({ applicationUuid, onClose }: ApplicationDetailsProps) {
  const { applications, updateApplicationStatus, deleteApplication } = useApplicationContext()
  const [isUpdating, setIsUpdating] = useState(false)
  const [isDeleting, setIsDeleting] = useState(false)
  const application = applications.find(app => app.uuid === applicationUuid)

  if (!application) return null

  const handleUpdateStatus = async (status: string) => {
    setIsUpdating(true)
    try {
      await updateApplicationStatus(applicationUuid, status as any)
    } catch (error) {
      console.error('Error updating application status:', error)
    } finally {
      setIsUpdating(false)
    }
  }

  const handleDeleteApplication = async () => {
    setIsDeleting(true)
    try {
      await deleteApplication(applicationUuid)
      onClose()
    } catch (error) {
      console.error('Error deleting application:', error)
    } finally {
      setIsDeleting(false)
    }
  }

  const renderTimeline = () => {
    const allDates = [
      { date: application.date_applied, event: "Applied" },
      { date: application.date_first_response, event: "First Response" },
      { date: application.date_rejected, event: "Rejected" },
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
            <Input type="date" value={application.date_applied} readOnly />
          </div>
          <div>
            <Label>Date of First Response</Label>
            <Input
              type="date"
              value={application.date_first_response || ''}
              onChange={(e) => handleUpdateStatus({ date_first_response: e.target.value })}
              disabled={isUpdating}
            />
          </div>
        </div>
        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="status">Status</Label>
            <Select
              value={application.status}
              onValueChange={(value) => handleUpdateStatus(value)}
              disabled={isUpdating}
            >
              <SelectTrigger id="status">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="prospect">Prospect</SelectItem>
                <SelectItem value="applied">Applied</SelectItem>
                <SelectItem value="interviewing">Interviewing</SelectItem>
                <SelectItem value="offered">Offered</SelectItem>
                <SelectItem value="accepted">Accepted</SelectItem>
                <SelectItem value="rejected">Rejected</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              value={application.description || ''}
              onChange={(e) => handleUpdateStatus({ description: e.target.value })}
              placeholder="Add your notes here..."
              disabled={isUpdating}
            />
          </div>
        </div>
        {renderTimeline()}
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