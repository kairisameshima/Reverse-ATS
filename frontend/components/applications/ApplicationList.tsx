'use client'

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { parse } from 'date-fns'
import { AlertCircle, ChevronRight } from 'lucide-react'
import { useState } from 'react'
import { useApplicationContext } from './ApplicationContext'


type ApplicationListProps = {
  applications: ReturnType<typeof useApplicationContext>['applications']
  onSelectApplication: (id: number) => void
}

export default function ApplicationListComponent({ applications, onSelectApplication }: ApplicationListProps) {
  const { updateApplicationStatus, shouldFollowUp } = useApplicationContext()
  const [updatingStatus, setUpdatingStatus] = useState<number | null>(null)

  const handleStatusChange = async (id: number, status: string) => {
    setUpdatingStatus(id)
    try {
      await updateApplicationStatus(id, status as any)
    } catch (error) {
      console.error('Error updating application status:', error)
    } finally {
      setUpdatingStatus(null)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Your Applications</CardTitle>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[300px]">
          {applications.map((app) => (
            <div key={app.id} className="flex items-center justify-between py-2 border-b last:border-b-0">
              <div>
                <h3 className="font-semibold">{app.company}</h3>
                <p className="text-sm text-muted-foreground">{app.position}</p>
                <p className="text-xs text-muted-foreground">Applied: {parse(app.dateApplied, "YYYY-MM-DD", new Date())}</p>
              </div>
              <div className="flex items-center space-x-2">
                {shouldFollowUp(app) && (
                  <AlertCircle className="h-4 w-4 text-yellow-500" title="Follow up needed" />
                )}
                <Select
                  value={app.status}
                  onValueChange={(value) => handleStatusChange(app.id, value)}
                  disabled={updatingStatus === app.id}
                >
                  <SelectTrigger className="w-[130px]">
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
                <Button variant="ghost" size="icon" onClick={() => onSelectApplication(app.id)}>
                  <ChevronRight className="h-4 w-4" />
                </Button>
              </div>
            </div>
          ))}
        </ScrollArea>
      </CardContent>
    </Card>
  )
}