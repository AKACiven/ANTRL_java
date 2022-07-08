package org.terasoluna.tourreservation.domain.service.tourinfo;

import java.util.Collections;
import java.util.List;

import javax.inject.Inject;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.terasoluna.tourreservation.domain.model.TourInfo;
import org.terasoluna.tourreservation.domain.repository.tourinfo.TourInfoRepository;
import org.terasoluna.tourreservation.domain.repository.tourinfo.TourInfoSearchCriteria;

@Service
@Transactional
public class TourInfoServiceImpl implements TourInfoService {

    @Inject
    TourInfoRepository tourInfoRepository;

    @Override
    public Page<TourInfo> searchTour(TourInfoSearchCriteria criteria,
            Pageable pageable) {

        long total = tourInfoRepository.countBySearchCriteria(criteria);
        List<TourInfo> content;
        if (0 < total) {
            content = tourInfoRepository.findPageBySearchCriteria(criteria,
                    pageable);
        } else {
            content = Collections.emptyList();
        }

        Page<TourInfo> page = new PageImpl<TourInfo>(content, pageable, total);
        return page;
    }
}