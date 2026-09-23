"""Election, Candidate, and Voter API routes."""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_role, get_current_user
from app.models.user import User
from app.schemas.election_schema import (
    ElectionCreate,
    ElectionUpdate,
    ElectionResponse,
    CandidateCreate,
    CandidateResponse,
    VoterAdd,
    VoterBulkAdd,
    VoterResponse,
)
from app.services.election_service import ElectionService

router = APIRouter(prefix="/api/elections", tags=["Elections"])


# --- Election CRUD ---
@router.post("/", response_model=ElectionResponse, status_code=201)
def create_election(
    data: ElectionCreate,
    current_user: User = Depends(require_role("SUPER_ADMIN", "ORG_ADMIN", "ELECTION_MANAGER")),
    db: Session = Depends(get_db),
):
    """Create a new election."""
    election = ElectionService.create_election(
        db,
        organization_id=data.organization_id,
        title=data.title,
        description=data.description,
        start_time=data.start_time,
        end_time=data.end_time,
        created_by=current_user.id,
    )
    candidates = ElectionService.get_candidates(db, election.id)
    return ElectionResponse(
        id=election.id,
        organization_id=election.organization_id,
        title=election.title,
        description=election.description,
        start_time=election.start_time,
        end_time=election.end_time,
        status=election.status,
        created_by=election.created_by,
        created_at=election.created_at,
        candidates=[CandidateResponse(
            id=c.id, election_id=c.election_id, name=c.name,
            description=c.description, created_at=c.created_at
        ) for c in candidates],
    )


@router.get("/", response_model=List[ElectionResponse])
def list_elections(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all elections."""
    elections = ElectionService.get_all_elections(db, skip=skip, limit=limit)
    result = []
    for e in elections:
        candidates = ElectionService.get_candidates(db, e.id)
        result.append(ElectionResponse(
            id=e.id, organization_id=e.organization_id, title=e.title,
            description=e.description, start_time=e.start_time, end_time=e.end_time,
            status=e.status, created_by=e.created_by, created_at=e.created_at,
            candidates=[CandidateResponse(
                id=c.id, election_id=c.election_id, name=c.name,
                description=c.description, created_at=c.created_at
            ) for c in candidates],
        ))
    return result


@router.get("/{election_id}", response_model=ElectionResponse)
def get_election(
    election_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get election by ID."""
    e = ElectionService.get_election(db, election_id)
    candidates = ElectionService.get_candidates(db, e.id)
    return ElectionResponse(
        id=e.id, organization_id=e.organization_id, title=e.title,
        description=e.description, start_time=e.start_time, end_time=e.end_time,
        status=e.status, created_by=e.created_by, created_at=e.created_at,
        candidates=[CandidateResponse(
            id=c.id, election_id=c.election_id, name=c.name,
            description=c.description, created_at=c.created_at
        ) for c in candidates],
    )


@router.put("/{election_id}", response_model=ElectionResponse)
def update_election(
    election_id: str,
    data: ElectionUpdate,
    current_user: User = Depends(require_role("SUPER_ADMIN", "ORG_ADMIN", "ELECTION_MANAGER")),
    db: Session = Depends(get_db),
):
    """Update an election (draft only)."""
    update_data = data.model_dump(exclude_unset=True)
    e = ElectionService.update_election(db, election_id, **update_data)
    candidates = ElectionService.get_candidates(db, e.id)
    return ElectionResponse(
        id=e.id, organization_id=e.organization_id, title=e.title,
        description=e.description, start_time=e.start_time, end_time=e.end_time,
        status=e.status, created_by=e.created_by, created_at=e.created_at,
        candidates=[CandidateResponse(
            id=c.id, election_id=c.election_id, name=c.name,
            description=c.description, created_at=c.created_at
        ) for c in candidates],
    )


@router.put("/{election_id}/activate")
def activate_election(
    election_id: str,
    current_user: User = Depends(require_role("SUPER_ADMIN", "ORG_ADMIN", "ELECTION_MANAGER")),
    db: Session = Depends(get_db),
):
    """Activate a draft election (must have ≥2 candidates)."""
    election = ElectionService.activate_election(db, election_id)
    return {"message": "Election activated", "status": election.status}


@router.put("/{election_id}/close")
def close_election(
    election_id: str,
    current_user: User = Depends(require_role("SUPER_ADMIN", "ORG_ADMIN", "ELECTION_MANAGER")),
    db: Session = Depends(get_db),
):
    """Close an active election."""
    election = ElectionService.close_election(db, election_id)
    return {"message": "Election closed", "status": election.status}


@router.delete("/{election_id}")
def delete_election(
    election_id: str,
    current_user: User = Depends(require_role("SUPER_ADMIN", "ORG_ADMIN")),
    db: Session = Depends(get_db),
):
    """Delete an election (not if active)."""
    return ElectionService.delete_election(db, election_id)


# --- Candidates ---
@router.post("/{election_id}/candidates", response_model=CandidateResponse, status_code=201)
def add_candidate(
    election_id: str,
    data: CandidateCreate,
    current_user: User = Depends(require_role("SUPER_ADMIN", "ORG_ADMIN", "ELECTION_MANAGER")),
    db: Session = Depends(get_db),
):
    """Add a candidate to an election (draft only)."""
    return ElectionService.add_candidate(db, election_id, data.name, data.description)


@router.get("/{election_id}/candidates", response_model=List[CandidateResponse])
def list_candidates(
    election_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List candidates for an election."""
    return ElectionService.get_candidates(db, election_id)


@router.delete("/candidates/{candidate_id}")
def remove_candidate(
    candidate_id: str,
    current_user: User = Depends(require_role("SUPER_ADMIN", "ORG_ADMIN", "ELECTION_MANAGER")),
    db: Session = Depends(get_db),
):
    """Remove a candidate (draft only)."""
    return ElectionService.delete_candidate(db, candidate_id)


# --- Voters ---
@router.post("/{election_id}/voters", response_model=VoterResponse, status_code=201)
def add_voter(
    election_id: str,
    data: VoterAdd,
    current_user: User = Depends(require_role("SUPER_ADMIN", "ORG_ADMIN", "ELECTION_MANAGER")),
    db: Session = Depends(get_db),
):
    """Add a voter to an election."""
    return ElectionService.add_voter(db, data.user_id, election_id)


@router.post("/{election_id}/voters/bulk", status_code=201)
def bulk_add_voters(
    election_id: str,
    data: VoterBulkAdd,
    current_user: User = Depends(require_role("SUPER_ADMIN", "ORG_ADMIN", "ELECTION_MANAGER")),
    db: Session = Depends(get_db),
):
    """Bulk add voters to an election."""
    added = []
    errors = []
    for uid in data.user_ids:
        try:
            voter = ElectionService.add_voter(db, uid, election_id)
            added.append(uid)
        except Exception as e:
            errors.append({"user_id": uid, "error": str(e)})
    return {"added": added, "errors": errors}


@router.get("/{election_id}/voters", response_model=List[VoterResponse])
def list_voters(
    election_id: str,
    current_user: User = Depends(require_role("SUPER_ADMIN", "ORG_ADMIN", "ELECTION_MANAGER")),
    db: Session = Depends(get_db),
):
    """List voters for an election."""
    return ElectionService.get_voters(db, election_id)


@router.delete("/{election_id}/voters/{user_id}")
def remove_voter(
    election_id: str,
    user_id: str,
    current_user: User = Depends(require_role("SUPER_ADMIN", "ORG_ADMIN", "ELECTION_MANAGER")),
    db: Session = Depends(get_db),
):
    """Remove a voter from an election."""
    return ElectionService.remove_voter(db, user_id, election_id)
