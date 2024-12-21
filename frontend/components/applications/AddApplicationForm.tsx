'use client'

import React, { useState } from 'react'
import { useApplicationContext } from './ApplicationContext'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Plus } from 'lucide-react'

export default function AddApplicationFormComponent() {
  const { addApplication } = useApplicationContext()
  const [newApplication, setNewApplication] = useState({ company: "", position: "", status: "prospect", dateApplied: "" })
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (newApplication.company && newApplication.position && newApplication.dateApplied) {
      setIsSubmitting(true)
      try {
        await addApplication(newApplication)
        setNewApplication({ company: "", position: "", status: "prospect", dateApplied: "" })
      } catch (error) {
        console.error('Error adding application:', error)
      } finally {
        setIsSubmitting(false)
      }
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Add New Application</CardTitle>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="company">Company</Label>
              <Input
                id="company"
                value={newApplication.company}
                onChange={(e) => setNewApplication({ ...newApplication, company: e.target.value })}
                placeholder="Enter company name"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="position">Position</Label>
              <Input
                id="position"
                value={newApplication.position}
                onChange={(e) => setNewApplication({ ...newApplication, position: e.target.value })}
                placeholder="Enter position"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="dateApplied">Date Applied</Label>
              <Input
                id="dateApplied"
                type="date"
                value={newApplication.dateApplied}
                onChange={(e) => setNewApplication({ ...newApplication, dateApplied: e.target.value })}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="status">Status</Label>
              <Select
                value={newApplication.status}
                onValueChange={(value) => setNewApplication({ ...newApplication, status: value as any })}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="prospect">Prospect</SelectItem>
                  <SelectItem value="applied">Applied</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
        <CardFooter>
          <Button type="submit" disabled={isSubmitting}>
            <Plus className="mr-2 h-4 w-4" /> {isSubmitting ? 'Adding...' : 'Add Application'}
          </Button>
        </CardFooter>
      </form>
    </Card>
  )
}